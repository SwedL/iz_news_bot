import requests
from bs4 import BeautifulSoup
import sqlite3
from pprint import pprint
from fake_useragent import FakeUserAgent

url = 'https://iz.ru/'

ua = FakeUserAgent()
headers = {
    'User-Agent': ua.random
}

# with open('iz_news', mode='w', encoding='utf-8') as f:
#     response = requests.get(url=url, headers=headers)
#     response.encoding = 'utf-8'
#     f.write(response.text)
#
# print(response.text)

with open('iz_news_text', 'r', encoding='utf-8') as f:
    input_data = f.read()
    # print(input_data)
    soup = BeautifulSoup(input_data, 'lxml')
    # print(soup)

# first_div = soup.find('div', 'four-col-news__list__row')
full_list_news = soup.find('div', 'show_views_and_comments')
article_title = full_list_news.find('div', 'node__cart__item__inside__info__title').text.strip()
article_image_url = 'https://' + full_list_news.find('img').get('data-src')[2:]
article_link = url + full_list_news.find('a', class_='node__cart__item__inside').get('href')
# print(full_list_news)
print(article_title)
print(article_image_url)
print(article_link)



