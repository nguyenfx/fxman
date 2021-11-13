import json
from datetime import datetime

import requests
from bs4 import BeautifulSoup

from con import Controller

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
ffsymbols = ["EURUSD", "GBPUSD", "AUDUSD", "NZDUSD", "USDJPY", "USDCHF", "USDCAD"]
ffurl = "https://www.forexfactory.com/explorerapi.php?content=positions&do=positions_graph_data&interval=D1&limit=2&currency="
mfurl = "https://www.myfxbook.com/community/outlook"
bnurl = "https://fapi.binance.com/futures/data/"
bnapis = {'topLongShortAccountRatio', 'topLongShortPositionRatio', 'globalLongShortAccountRatio'}

con = Controller()


def FFfetch():
    for symbol in ffsymbols:
        response = requests.get(ffurl + symbol, headers=headers)
        detail = json.loads(response.text)
        positions = detail["positions"]
        position = positions[-1]
        traders_is_low = position["traders_is_low"]
        weekend = position["weekend"]
        if not traders_is_low and not weekend:
            lots_ratio = int(position["lots_ratio"])
            traders_ratio = int(position["traders_ratio"])
            value = lots_ratio - 50 + traders_ratio - 50
            con.upsert_sentiment(symbol, value)
            if not value == 0:
                print(symbol, value)


def MFfetch():
    response = requests.get(mfurl, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    tbody = soup.find(id="outlookSymbolsTableContent")
    trs = tbody.find_all(class_="outlook-symbol-row")
    for tr in trs:
        symbol = tr.get("symbolname")
        shortbar = tr.find("div", class_="progress-bar progress-bar-danger")
        longbar = tr.find("div", class_="progress-bar progress-bar-success")
        short = int(shortbar.get("style")[-4:-2])
        long = int(longbar.get("style")[-4:-2])
        value = long - short
        con.upsert_sentiment(symbol, value)


def BNfetch():
    symbol = "BTCUSD"
    sumratio = 0
    for api in bnapis:
        response = requests.get(bnurl + api + "?symbol=BTCUSDT&period=4h", headers=headers)
        rows = json.loads(response.text)
        ratio = float(rows[-1]['longShortRatio'])
        sumratio += ratio
    value = int((sumratio / 3 - 1) / (sumratio / 3 + 1) * 100)
    con.upsert_sentiment(symbol, value)


def fetch():
    # FFfetch()
    MFfetch()
    BNfetch()
    today = datetime.utcnow()
    epoch = datetime(1970, 1, 1)
    timestamp = (today - epoch).total_seconds()
    con.upsert_sentiment("Time", int(timestamp))
    sentiments = con.get_sentiments()
    print(json.dumps(sentiments))
    file = open('static/sentiments.txt', 'w')
    file.writelines(json.dumps(sentiments))
    file.close()
    print("Sentiment fetch done, tested:", " EURUSD:", con.get_sentiment("EURUSD")[0], " XAUUSD:",
          con.get_sentiment("XAUUSD")[0], " BTCUSD:", con.get_sentiment("BTCUSD")[0])


if __name__ == "__main__":
    fetch()
