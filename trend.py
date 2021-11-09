import datetime
import json
import requests


class Symbol:
    symbols = {"EURUSD": 0, "GBPUSD": 0, "AUDUSD": 0, "NZDUSD": 0, "USDJPY": 0, "USDCHF": 0, "USDCAD": 0}


url = 'https://www.forexfactory.com/explorerapi.php?content=positions&do=positions_graph_data&interval=D1&limit=2&currency='
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


def fetch():
    for symbol in Symbol.symbols:
        Symbol.symbols[symbol] = 0
        response = requests.get(url + symbol, headers=headers)
        detail = json.loads(response.text)
        positions = detail["positions"]
        for position in positions:
            day = position["datetime"]
            year = int(day["year"])
            month = int(day["month"])
            date = int(day["date"])
            current = datetime.datetime.now()
            if current.year == year and current.month == month and current.day == date:
                lots_ratio = position["lots_ratio"]
                traders_ratio = position["traders_ratio"]
                if lots_ratio > 55 and traders_ratio > 55:
                    Symbol.symbols[symbol] = 1
                elif lots_ratio < 55 and traders_ratio < 55:
                    Symbol.symbols[symbol] = -1
                break
    print(Symbol.symbols)


def get(symbol):
    return Symbol.symbols[symbol]


if __name__ == "__main__":
    fetch()
