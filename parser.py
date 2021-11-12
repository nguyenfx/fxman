from bs4 import BeautifulSoup
import requests, json

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
    }

response = requests.get("http://45.32.116.92/fxman/accounts", headers=headers)
print(response.text)

