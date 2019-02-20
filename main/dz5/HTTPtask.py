from requests import get
from json import dumps


def exchange_rates(currency_abbreviation: str) -> float:

    data = get(f"http://www.nbrb.by/API/ExRates/Rates/{currency_abbreviation}?ParamMode=2")

    if data.status_code == 404:
        raise ValueError(f"Currency '{currency_abbreviation}' not found")

    rate = data.json()["Cur_OfficialRate"]
    scale = data.json()["Cur_Scale"]

    return 1 / rate * scale


def get_weather():

    data = get("https://yandex.by/pogoda/region/149")

    print(data.text)


