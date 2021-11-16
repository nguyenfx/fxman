import chart
from con import Controller
import sen, json

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


if __name__ == "__main__":
    ff_fetch()

