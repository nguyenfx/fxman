import chart
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

if __name__ == "__main__":
    handle = TA_Handler(
        symbol="BTCUSDT",
        screener="crypto",
        exchange="BINANCE",
        interval=Interval.INTERVAL_4_HOURS
    )
    analysis = handle.get_analysis()
    print(analysis.indicators["close"])