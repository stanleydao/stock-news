import requests
from datetime import datetime
import os
from twilio.rest import Client
# from twilio.http.http_client import TwilioHttpClient

account_sid = "AC667dcae38f51fd650ffb369ab4e0955d"
auth_token = "94c6a799ee4941657ea89318ab8f0d6b"

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
  return news_articles


def send_news(news_articles):
  for article in news_articles:
    # proxy_client = TwilioHttpClient()
    # proxy_client.session.proxies = {'https': os.environ['https_proxy']}
    # client = Client(account_sid, auth_token, http_client=proxy_client)
    client = Client(account_sid, auth_token)
    if percentage_difference > 0:
      emoji = "⬆️"
    if percentage_difference < 0:
      emoji = "⬇️"
    message = client.messages.create(
        body=f"{STOCK_NAME}{emoji}{round(abs(percentage_difference))}%\nHeadline: {article['title']}\nLink:{article['url']}",
        from_='+12563051627',
        to='+15146294888'
    )
    print(message.status)


if abs(percentage_difference) > 5:
  news = get_news()
  send_news(news)
