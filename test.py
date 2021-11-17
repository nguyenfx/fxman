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

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

if __name__ == "__main__":
    response = requests.get("https://www.dailyfx.com/sentiment-report", headers=headers)
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
        con.upsert_sentiment("df", symbol, sentiment, contrarian)

