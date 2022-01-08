import requests
from datetime import datetime

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = "Y6E6KZFQ538F6E42"
NEWS_API_KEY = "6b43a9a86e2e4eb49238a3601ba9f593"

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


percentage_difference = ((last_day_price-before_yesterday_price)/last_day_price)*100


def get_news():
  today_date = str(datetime.today()).split(" ")[0]
  news_parameters = {
    "q": COMPANY_NAME,
    "from":today_date,
    "sortBy":"popularity",
    "apikey": NEWS_API_KEY
  }
  news_reponse = requests.get(url=NEWS_ENDPOINT, params=news_parameters)
  news_reponse.raise_for_status()
  news_data = news_reponse.json()
  news_articles = news_data["articles"][:3]

  print(news_articles)


if abs(percentage_difference) > 1:
  get_news()
