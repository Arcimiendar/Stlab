from flask import Flask, render_template, request
from flask.json import dump, load
import requests

app = Flask(__name__)


def update_currencies():

    with open('currencies.JSON', 'w') as currency_file:
        currency_data = requests.get('http://www.nbrb.by/API/ExRates/Currencies').json()

        currency_data = sorted(currency_data, key=lambda currency: currency['Cur_Abbreviation'])

        data_without_repeats = []

        for currency in currency_data:

            already_represented = False
            for item in data_without_repeats:
                if item['Cur_Abbreviation'] == currency['Cur_Abbreviation']\
                   or item['Cur_Name_Eng'] == currency['Cur_Name_Eng']:
                    already_represented = True

            if already_represented:
                continue

            data_without_repeats.append(currency)

        dump(data_without_repeats, currency_file)


@app.route("/", methods=["GET"])
def main_page():
    return render_template("index.html")


@app.route("/update_currencies/")
def update_currencies_data():
    update_currencies()
    return "currencies are updated!"


@app.route("/get_selector")
def get_currencies():
    with open("currencies.JSON", 'r') as json_file:
        currencies_json = load(json_file)

    return render_template("selector.html", currencies=currencies_json)


@app.route('/<string:currency>/<string:abbreviation>/<int:send_amount>/')
def get_convert_result(currency: str, abbreviation: str, send_amount: int):

    rate_info = requests.get(f'http://www.nbrb.by/API/ExRates/Rates/{abbreviation}',
                             params={'ParamMode': 2})

    rate = float(rate_info.json()['Cur_OfficialRate'])
    amount = float(rate_info.json()['Cur_Scale'])

    print(currency)

    if currency == "foreign":
        message = f'{send_amount} {abbreviation} equal to ' \
                  f'{round(int(send_amount) * rate / amount, 2)} in BYN'
    elif currency == "byn":
        message = f'{send_amount} BYN equal to {round(int(send_amount) * amount / rate, 2)}' \
                  f' in {abbreviation}'
    else:
        return "Error 404. Page not found", 404

    return message


update_currencies()  # load currencies in the first time
app.run()
