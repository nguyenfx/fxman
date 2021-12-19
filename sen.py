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
fcsurl = "https://storage.googleapis.com/public-sentiments-v4/fxcs-sentiments.json"
dfurl = "https://www.dailyfx.com/sentiment-report"

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
        con.upsert_sentiment("fc", symbol, sentiment, 0)
        # con.upsert_sentiment("fc", symbol, sentiment, contrarian)


def df_fetch():
    response = requests.get(dfurl, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    content = soup.find(class_="dfx-articleBody__content")
    rows = content.find_all("tr")
    for row in rows[1:]:
        symbol_row = row.find("td", {"data-heading": "SYMBOL"})
        symbol_span = symbol_row.find(class_="gsstx")
        symbol = symbol_span.text.replace("/", "").strip()
        bias_row = row.find("td", {"data-heading": "TRADING BIAS"})
        bias_span = bias_row.find(class_="gsstx")
        bias = bias_span.text.strip()
        if bias == "BULLISH":
            contrarian = 1
        elif bias == "BEARISH":
            contrarian = -1
        else:
            contrarian = 0
        long_row = row.find("td", {"data-heading": "NET-LONG%"})
        long_span = long_row.find(class_="gsstx")
        long = int(long_span.text.strip()[:-4])
        short_row = row.find("td", {"data-heading": "NET-SHORT%"})
        short_span = short_row.find(class_="gsstx")
        short = int(short_span.text.strip()[:-4])
        sentiment = long -short
        con.upsert_sentiment("df", symbol, sentiment, 0)
        # con.upsert_sentiment("df", symbol, sentiment, contrarian)


def bn_fetch(name):
    sum = 0
    for api in bnapis:
        response = requests.get(bnurl + api + "?symbol=" + name + "USDT&period=1h", headers=headers)
        rows = json.loads(response.text)
        if api == "topLongShortPositionRatio":
            sum += float(rows[-1]['longShortRatio']) * 2
        else:
            sum += float(rows[-1]['longShortRatio'])
    ratio = sum / (len(bnapis) + 1)
    sentiment = int((ratio - 1) / (ratio + 1) * 100)
    con.upsert_sentiment("bn", name + "USD", sentiment, 0)


def fetch():
    ff_fetch()
    mf_fetch()
    fc_fetch()
    df_fetch()
    bn_fetch("BTC")
    bn_fetch("ETH")
    sentiments = con.get_sentiments()
    print(json.dumps(sentiments))


if __name__ == "__main__":
    fetch()
