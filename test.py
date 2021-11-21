from datetime import datetime

import chart
import ta
from con import Controller
import sen, json

from tradingview_ta import TA_Handler, Interval

import requests
from bs4 import BeautifulSoup
from sen import ff_fetch

con = Controller()

def test_all():
    sen.fetch()
    chart.gen_chart()
    signal = con.get_signal("CADJPY")
    print(signal)
    sentiments = con.get_sentiments()
    print(sentiments)
    status = con.get_status()
    print(status)
    con.calculate_all_statistic()
    accounts = con.get_accounts()
    for account in accounts:
        number = account[0]
        stats = con.get_statistic(number)
        print(stats)

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
bnurl = "https://fapi.binance.com/futures/data/"
bnapis = ['topLongShortAccountRatio', 'topLongShortPositionRatio', 'globalLongShortAccountRatio']

def fetch(name):
    response = requests.get(bnurl + bnapis[0] + "?symbol=" + name + "USDT&period=1d", headers=headers)
    rows0 = json.loads(response.text)
    response = requests.get(bnurl + bnapis[1] + "?symbol=" + name + "USDT&period=1d", headers=headers)
    rows1 = json.loads(response.text)
    response = requests.get(bnurl + bnapis[2] + "?symbol=" + name + "USDT&period=1d", headers=headers)
    rows2 = json.loads(response.text)
    for i in range(len(rows0)):
        date0 = datetime.fromtimestamp(rows0[i]['timestamp'] / 1000)
        date1 = datetime.fromtimestamp(rows1[i]['timestamp'] / 1000)
        date2 = datetime.fromtimestamp(rows2[i]['timestamp'] / 1000)
        sum = float(rows0[i]['longShortRatio']) + float(rows1[i]['longShortRatio']) * 2 + float(rows2[i]['longShortRatio'])
        ratio = sum / 4
        sentiment = int((ratio - 1) / (ratio + 1) * 100)
        con.upsert_sentiment_date('bn', name + "USD", sentiment, 0, date0.strftime('%Y-%m-%d'))
        con.upsert_sentiment_date('avg', name + "USD", sentiment, 0, date0.strftime('%Y-%m-%d'))
        print(date0.strftime('%Y-%m-%d'), sentiment)


if __name__ == "__main__":
    fetch("BTC")
    fetch("ETH")