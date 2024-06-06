from bs4 import BeautifulSoup
import sqlite3
from pprint import pprint

url = 'https://iz.ru/'
db = sqlite3.connect('news.db')
cursor = db.cursor()

with db:
    cursor.execute("""CREATE TABLE IF NOT EXISTS news (
        summary text,
        date_time text
    )""")

with open('iz_news', 'r', encoding='utf-8') as f:
    input_data = f.read()
    soup = BeautifulSoup(input_data, 'html.parser')

full_list_news = soup.find_all('div', 'node__cart__item show_views_and_comments')

list_processed_news = []

for new in full_list_news:
    temp_dict = {
        'image': 'https://' + new.find('img').get('data-src')[2:],
        'category': new.find('a').text,
        'description': new.find('div', 'node__cart__item__inside__info__title small-title-style1').text.strip(),
        'date_time': new.time.get('datetime'),
        'link': url[:-1] + new.find('a', class_='node__cart__item__inside').get('href'),
    }
    list_processed_news.append(temp_dict)
pprint(list_processed_news)

with db:
    news_bd = [i[0] for i in cursor.execute("SELECT description FROM news")]
    for new in list_processed_news:
        if new['description'] not in news_bd:
            cursor.execute("""INSERT INTO news (description, date_time)
                VALUES (:description, :date_time)
            """, new)


# print(list(news_bd))
