import json

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
fcsurl = "https://storage.googleapis.com/public-sentiments-v3/fxcs-sentiments.json"

con = Controller()


def ff_fetch():
    for symbol in ffsymbols:
        response = requests.get(ffurl + symbol, headers=headers)
        detail = json.loads(response.text)
        positions = detail["positions"]
        position = positions[-1]
        lots_ratio = int(position["lots_ratio"])
        traders_ratio = int(position["traders_ratio"])
        sentiment = lots_ratio - 50 + traders_ratio - 50
        con.upsert_sentiment("ff", symbol, sentiment, 0)


def mf_fetch():
    response = requests.get(mfurl, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    tbody = soup.find(id="outlookSymbolsTableContent")
    trs = tbody.find_all(class_="outlook-symbol-row")
    for tr in trs:
        symbol = tr.get("symbolname")
        short_bar = tr.find("div", class_="progress-bar progress-bar-danger")
        long_bar = tr.find("div", class_="progress-bar progress-bar-success")
        short = int(short_bar.get("style")[-4:-2])
        long = int(long_bar.get("style")[-4:-2])
        sentiment = long - short
        con.upsert_sentiment("mf", symbol, sentiment, 0)


def fc_fetch():
    response = requests.get(fcsurl, headers=headers)
    data = json.loads(response.text)
    sentiments = data["sentiments"]
    for row in sentiments:
        symbol = row["instrument"].replace("/", "")
        short_percentage = int(row["short_percentage"])
        long_percentage = int(row["long_percentage"])
        sentiment = long_percentage - short_percentage
        if row["contrarian_indicator_signal"] == "UP":
            contrarian = 1
        elif row["contrarian_indicator_signal"] == "DOWN":
            contrarian = -1
        else:
            contrarian = 0
        con.upsert_sentiment("fc", symbol, sentiment, contrarian)


def bn_fetch():
    symbol = "BTCUSD"
    sumratio = 0
    for api in bnapis:
        response = requests.get(bnurl + api + "?symbol=BTCUSDT&period=4h", headers=headers)
        rows = json.loads(response.text)
        ratio = float(rows[-1]['longShortRatio'])
        sumratio += ratio
    sentiment = int((sumratio / 3 - 1) / (sumratio / 3 + 1) * 100)
    con.upsert_sentiment("bn", symbol, sentiment, 0)


def fetch():
    ff_fetch()
    mf_fetch()
    fc_fetch()
    bn_fetch()
    sentiments = con.get_sentiments()
    print(json.dumps(sentiments))


if __name__ == "__main__":
    fetch()
