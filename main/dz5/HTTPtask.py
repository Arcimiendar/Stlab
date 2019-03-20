from requests import get
import re


def exchange_rates(currency_abbreviation: str) -> float:

    data = get(f"http://www.nbrb.by/API/ExRates/Rates/{currency_abbreviation}?ParamMode=2")

    if data.status_code == 404:
        raise ValueError(f"Currency '{currency_abbreviation}' not found")

    rate = data.json()["Cur_OfficialRate"]
    scale = data.json()["Cur_Scale"]

    return 1 / rate * scale


def get_weather():

    pattern_page = r"<a class=\"link link_theme_normal " \
              r"place-list__item-name i-bem\" tabindex=\"0\" href=\"" \
              r"(?P<ref>/pogoda/[a-z-]*)\" (?:[\w-]*)='{\"link\":{}}'>" \
              r"(?P<name>[А-ЯЁ][ёа-я]+(?:[ -][ЁА-Я][ёа-я]+)?)</a>"

    pattern_temperature = r"(?<=<div class=\"temp fact__temp fact__temp_size_s\"><span class=\"temp_" \
                          r"_value\">)(?:\+)?(?P<temprt>[−]?[0-9]+)(?=</span><span class=\"temp__unit" \
                          r" i-font i-font_face_yandex-sans-text-medium\">°</span></div>)"
    data = get("https://yandex.by/pogoda/region/149")
    cities = re.findall(pattern_page, data.text)

    weather_dict = {}

    for city in cities:
        url = "https://yandex.by" + city[0]

        data = get(url)

        value = re.search(pattern_temperature, data.text)[0]

        if value[0] == chr(8722):
            value = -1 * int(value[1:])

        weather_dict[city[1]] = int(value)

    return weather_dict
