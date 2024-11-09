from flask import Flask, render_template, request, redirect, url_for, flash
from forms import UserInputForm
import ssl
import certifi
import json
from urllib.request import urlopen

app = Flask(__name__)
app.secret_key = 'APIProject2024Dec'  # Use a secure key for production.

def get_jsonparsed_data(url):
    context = ssl.create_default_context(cafile=certifi.where())
    response = urlopen(url, context=context)
    data = response.read().decode("utf-8")
    return json.loads(data)

@app.route("/", methods=["GET", "POST"])
def form():
    form = UserInputForm()
    if request.method == "POST" and form.validate_on_submit():
        stock_symbol = form.query.data.strip().upper()
        selected_financial_data = form.financial_data_choice.data
        selected_exchange = form.exchange.data
        apikey = "fioy1PNYdUolrtu1JxezOPT5MVgkJjVR"

        # API URLs for stock data
        quote_url = f"https://financialmodelingprep.com/api/v3/quote/{stock_symbol}?apikey={apikey}"
        income_statement_url = f"https://financialmodelingprep.com/api/v3/income-statement/{stock_symbol}?apikey={apikey}"

        try:
            general_data = get_jsonparsed_data(quote_url)
            financial_data = get_jsonparsed_data(income_statement_url)

            profile_data = general_data[0] if general_data and isinstance(general_data, list) else {}
            financial_details = financial_data[0] if financial_data and isinstance(financial_data, list) else {}

            combined_data = {
                "profile": profile_data,
                "financials": financial_details
            }

            price_data = {
                "labels": ['Price', 'Day High', 'Day Low', 'Year High'],
                "values": [
                    profile_data.get('price', 0),
                    profile_data.get('dayHigh', 0),
                    profile_data.get('dayLow', 0),
                    profile_data.get('yearHigh', 0)
                ]
            }

            return render_template(
                "processed_results.html",
                combined_data=combined_data,
                price_data=json.dumps(price_data),
                financial_data_choice=selected_financial_data,
                stock_symbol=stock_symbol,
                exchange=selected_exchange
            )

        except Exception as e:
            flash("An error occurred while fetching data.")
            print("Error:", e)
            return redirect(url_for("form"))

    return render_template("form.html", form=form)

@app.route("/home")
def home():
    return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True)
