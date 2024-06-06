from fake_useragent import FakeUserAgent
from bs4 import BeautifulSoup
import requests

ua = FakeUserAgent()
url = 'https://iz.ru/news'


req = requests.get(
        url=url,
        headers={'User-Agent': ua.random}
    )

req.encoding = "utf-8"

with open("iz_news", 'w', encoding="utf-8") as file:
    file.write(req.text)

print(req.content)
