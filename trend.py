from bs4 import BeautifulSoup
import requests
import json


class Symbol:
    ffsymbols = {"EURUSD": 0, "GBPUSD": 0, "AUDUSD": 0, "NZDUSD": 0, "USDJPY": 0, "USDCHF": 0, "USDCAD": 0}
    mfsymbols = {}
    bnsymbols = {}


ffurl = "https://www.forexfactory.com/explorerapi.php?content=positions&do=positions_graph_data&interval=D1&limit=2&currency="
mfurl = "https://www.myfxbook.com/community/outlook"
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


def FFfetch():
    for symbol in Symbol.ffsymbols:
        Symbol.ffsymbols[symbol] = 0
        response = requests.get(ffurl + symbol, headers=headers)
        detail = json.loads(response.text)
        positions = detail["positions"]
        position = positions[-1]
        traders_is_low = position["traders_is_low"]
        weekend = position["weekend"]
        if not traders_is_low and not weekend:
            lots_ratio = int(position["lots_ratio"])
            traders_ratio = int(position["traders_ratio"])
            Symbol.ffsymbols[symbol] = (lots_ratio - 50 + traders_ratio - 50)
    print(Symbol.ffsymbols)


def FFget(symbol):
    return Symbol.ffsymbols.get(symbol)


def MFfetch():
    response = requests.get(mfurl, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    tbody = soup.find(id="outlookSymbolsTableContent")
    trs = tbody.find_all(class_="outlook-symbol-row")
    Symbol.mfsymbols.clear()
    for tr in trs:
        symbol = tr.get("symbolname")
        shortbar = tr.find("div", class_="progress-bar progress-bar-danger")
        longbar = tr.find("div", class_="progress-bar progress-bar-success")
        short = int(shortbar.get("style")[-4:-2])
        long = int(longbar.get("style")[-4:-2])
        Symbol.mfsymbols[symbol] = long - short
    print(Symbol.mfsymbols)


def MFget(symbol):
    return Symbol.mfsymbols.get(symbol)


def BNfetch():
    Symbol.bnsymbols.clear()
    apis = {'topLongShortAccountRatio', 'topLongShortPositionRatio', 'globalLongShortAccountRatio'}
    sumratio = 0
    for api in apis:
        response = requests.get("https://fapi.binance.com/futures/data/" + api + "?symbol=BTCUSDT&period=4h",
                                headers=headers)
        rows = json.loads(response.text)
        ratio = float(rows[-1]['longShortRatio'])
        sumratio += ratio
    trend = int((sumratio / 3 - 1) / (sumratio / 3 + 1) * 100)
    Symbol.bnsymbols["BTCUSD"] = trend
    print(Symbol.bnsymbols)


def BNget(symbol):
    return Symbol.bnsymbols.get(symbol)


def fetch():
    FFfetch()
    MFfetch()
    BNfetch()


def get(symbol):
    ff = FFget(symbol)
    mf = MFget(symbol)
    bn = BNget(symbol)
    if ff and mf:
        return int((ff + mf) / 2)
    elif ff and not mf:
        return ff
    elif not ff and mf:
        return mf
    elif bn:
        return bn
    else:
        return 0


if __name__ == "__main__":
    fetch()
    print(get("EURUSD"), get("GBPUSD"), get("XAUUSD"), get("BTCUSD"))