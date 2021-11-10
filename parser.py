from bs4 import BeautifulSoup
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
r = requests.get("https://www.myfxbook.com/community/outlook", headers=headers)
soup = BeautifulSoup(r.content, 'html.parser')
tbody = soup.find(id="outlookSymbolsTableContent")
trs = tbody.find_all(class_="outlook-symbol-row")
for tr in trs:
    symbol = tr.get("symbolname")
    shortbar = tr.find("div", class_="progress-bar progress-bar-danger")
    longbar = tr.find("div", class_="progress-bar progress-bar-success")
    short = int(shortbar.get("style")[-4:-2])
    long = int(longbar.get("style")[-4:-2])
    print(symbol, long - short)

