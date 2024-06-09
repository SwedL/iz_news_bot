from typing import List

from bs4 import BeautifulSoup
from telebot import formatting
from datetime import datetime, timedelta
from pathlib import Path
from news_sources.base_news_sources import BaseNewsSource
from news_sources.types import NewsData
from pprint import pprint
import sqlite3

# db = sqlite3.connect('news.db')
# cursor = db.cursor()
#
# with db:
#     cursor.execute("""CREATE TABLE IF NOT EXISTS news (
#         summary text,
#         date_time text
#     )""")


class IZNewsSource(BaseNewsSource):
    SOURCE_MAIN_URL = 'https://iz.ru/news'
    SOURCE = 'ИЗВЕСТИЯ IZ'
    HASHTAG = 'НОВОСТИ IZ '
    DEFAULT_IMAGE_URL = 'https://cdn.iz.ru/sites/default/files/styles/310x220/public/default_images/DefaultPic11.jpg?itok=5sTOtm7a'

    def __init__(self):
        super().__init__(url=self.SOURCE_MAIN_URL)

    def get_news(self):
        raw_news = self._get_raw_today_news()
        self._raw_news_list(raw_news=raw_news)
        self._filter_actual_news()
        self._sorted_news_list()
        self._saving_news_to_database()

    def _get_raw_today_news(self) -> List[BeautifulSoup]:
        # res = self.parsed_source.find_all('div', 'node__cart__item show_views_and_comments')
        res = self.parsed_source.find_all('div', 'node__cart__item show_views_and_comments')
        return res

    def _raw_news_list(self, raw_news: List[BeautifulSoup]) -> None:
        self.list_processed_news.clear()  # предварительно очищаем список обработанных новостей
        for news in raw_news:
            current_news = {
                'category': self._get_article_category(news),
                'summary': self._get_article_summary(news),
                'image_url': self._get_article_image_url(news),
                'link': self._get_article_link(news),
                'datetime': self._get_article_datetime(news),
            }
            self.list_processed_news.append(current_news)

    def _sorted_news_list(self):
        self.list_processed_news.sort(key=lambda x: datetime(*map(int, x['datetime'].split())))

    def _saving_news_to_database(self) -> None:
        rows_for_db = [tuple(n.values()) for n in self.list_processed_news]
        with self.db:
            self.cursor.executemany("""INSERT INTO news (category, summary, image_url, link, datetime)
            VALUES (?, ?, ?, ?, ?) """, rows_for_db)

    def _filter_actual_news(self) -> None:
        with self.db:
            self.cursor.execute("SELECT * FROM news")
            db_news = self.cursor.fetchall()
            self.list_processed_news = list(filter(lambda n: tuple(n.values()) not in db_news, self.list_processed_news))

    def _get_article_category(self, news: BeautifulSoup) -> str:
        return news.find('a').text

    def _get_article_summary(self, news: BeautifulSoup) -> str:
        return news.find('div', 'node__cart__item__inside__info__title small-title-style1').text.strip()

    def _get_article_image_url(self, news: BeautifulSoup) -> str:
        return 'https://' + news.find('img').get('data-src')[2:]

    def _get_article_link(self, news: BeautifulSoup) -> str:
        first_part_url = self.SOURCE_MAIN_URL.rpartition('/')[0]
        return first_part_url + news.find('a', class_='node__cart__item__inside').get('href')

    def _get_article_datetime(self, news: BeautifulSoup) -> str:
        datetime_text = news.time.get('datetime')
        for symbol in '-ZT:':
            while symbol in datetime_text:
                datetime_text = datetime_text.replace(symbol, ' ')
        return datetime_text.strip()

    def caption_message(self, news: dict) -> str:
        category = news['category']
        summary = news['summary']
        link = news['link']
        row_list_message = [f'{formatting.hbold(category)}',
                            summary,
                            f'подробнее {formatting.hlink(" здесь ", link)}',
                            f'Источник: {formatting.hlink(self.SOURCE, self.SOURCE_MAIN_URL)}',
                            self._get_footer(),
                            ]
        return '\n\n'.join(row_list_message)

    def _get_footer(self):
        return f'#{self.HASHTAG} {formatting.hlink("Подписаться", "https://t.me/+pxWMeyikCNdjOGNi")}'


if __name__ == '__main__':
    iz = IZNewsSource()
    iz.get_news()
    pprint(iz.list_processed_news)
    print(len(iz.list_processed_news))
