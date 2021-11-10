from bs4 import BeautifulSoup
import requests, json

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
    }
apis = {'topLongShortAccountRatio', 'topLongShortPositionRatio', 'globalLongShortAccountRatio'}
sumratio = 0
for api in apis:
    response = requests.get("https://fapi.binance.com/futures/data/" + api + "?symbol=BTCUSDT&period=1h", headers=headers)
    rows = json.loads(response.text)
    print(rows[-1])
    ratio = float(rows[-1]['longShortRatio'])
    sumratio += ratio
n = sumratio / 3
m = int((sumratio / 3 - 1) / (sumratio / 3 + 1) * 100)
print(m)

