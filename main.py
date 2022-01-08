import requests

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = "Y6E6KZFQ538F6E42"

stock_parameters = {
  "function": "TIME_SERIES_DAILY",
  "symbol": STOCK_NAME,
  "apikey": STOCK_API_KEY
}

stock_response = requests.get(url=STOCK_ENDPOINT, params=stock_parameters)
stock_response.raise_for_status()

stock_data = stock_response.json()
time_series = stock_data['Time Series (Daily)']
closing_prices = [float(value['4. close']) for (day, value) in time_series.items()]
last_two_closing = closing_prices[:2]
last_day_price = last_two_closing[0]
before_yesterday_price = last_two_closing[1]
