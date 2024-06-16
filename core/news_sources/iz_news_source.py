import asyncio
from typing import List, Dict
import sqlite3
from bs4 import BeautifulSoup
from datetime import datetime
from core.news_sources.base_news_sources import BaseNewsSource
from pathlib import Path
from aiogram.utils.markdown import hlink
from fake_useragent import FakeUserAgent
import aiohttp


class IZNewsSource:
    DATABASE = Path(__file__).parent.parent.parent / 'iz_news.db'
    SOURCE_MAIN_URL = 'https://iz.ru/news'
    SOURCE = 'ИЗВЕСТИЯ IZ'
    HASHTAG = 'НОВОСТИ_IZ '
    DEFAULT_IMAGE_URL = 'https://cdn.iz.ru/sites/default/files/styles/310x220/public/default_images/DefaultPic11.jpg?itok=5sTOtm7a'

    def __init__(self):
        self.db = None
        self.cursor = None
        self.parsed_source = None
        self.list_processed_news = []
        self.news_category_filter = ['Мир', 'Общество', 'Происшествия', 'Здоровье', 'Армия',
                                     'Экономика', 'Политика', 'Недвижимость', 'Авто', 'Культура',
                                     'Пресс-релизы', 'Спорт', 'Наука и техника', 'Туризм']

    # Создаём базу данных для хранения ранее опубликованных новостей, если она ещё не создана
    def create_database(self):
        """Создание базы данных для определения опубликованных ранее новостей"""
        self.db = sqlite3.connect(self.DATABASE)
        self.cursor = self.db.cursor()
        with self.db:
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS iz_news (
            category text,
            summary text,
            image_url text,
            link text,
            datetime text
            )""")

    @staticmethod
    def get_headers() -> Dict[str, str]:
        ua = FakeUserAgent()
        return {
            'User-Agent': ua.random
        }

    async def get_parsed_source(self) -> BeautifulSoup:
        """Получаем содержимое страницы источника новостей"""
        async with aiohttp.ClientSession() as session:
            async with session.get(url=self.SOURCE_MAIN_URL, headers=self.get_headers()) as response:
                text = await response.text()
                return BeautifulSoup(text, features='html.parser')

    async def get_news(self):
        self.parsed_source = await self.get_parsed_source()  # получаем содержимое страницы новостей
        self.news_list()  # формируем список обработанных новостей
        self.sorted_news_list()  # сортируем новости согласно времени их выхода
        await asyncio.sleep(0)

    def get_raw_today_news(self) -> List[BeautifulSoup]:
        """Получаем список сырых новостей, из контента страницы, согласно классу тега"""
        return self.parsed_source.find_all('div', 'node__cart__item show_views_and_comments')

    def news_list(self) -> None:
        """Формируем список обработанных новостей из списка сырых новостей"""
        self.list_processed_news.clear()  # при новом парсинге, очищаем старый список обработанных новостей
        for news in self.get_raw_today_news():
            current_news = {
                'category': self.get_article_category(news),
                'summary': self.get_article_summary(news),
                'image_url': self.get_article_image_url(news),
                'link': self.get_article_link(news),
                'datetime': self.get_article_datetime(news),
            }
            self.list_processed_news.append(current_news)

    def filter_category(self) -> None:
        """Фильтруем новости, согласно списку выбранных рубрик в чат-боте"""
        self.list_processed_news = list(
            filter(lambda n: n['category'] in self.news_category_filter, self.list_processed_news))

    def filter_actual_news(self) -> None:
        """Оставляем в списке обработанных новостей новости, которые ранее небыли опубликованы"""
        with self.db:
            self.cursor.execute("SELECT * FROM iz_news")
            db_news = self.cursor.fetchall()
            self.list_processed_news = list(
                filter(lambda n: tuple(n.values()) not in db_news, self.list_processed_news))

    def sorted_news_list(self):
        """Сортируем список обработанных новостей согласно их дате и времени выхода"""
        self.list_processed_news.sort(key=lambda x: datetime(*map(int, x['datetime'].split())))

    def saving_news_to_database(self) -> None:
        """Сохраняем свежие новости в базу данных для последующего определения опубликованных ранее новостей """
        # выбираем только свежие новости из списка новостей
        self.filter_actual_news()
        # сохраняем свежие новости в базу данных
        rows_for_db = [tuple(n.values()) for n in self.list_processed_news]
        with self.db:
            self.cursor.executemany("""INSERT INTO iz_news (category, summary, image_url, link, datetime)
            VALUES (?, ?, ?, ?, ?) """, rows_for_db)

    def clear_data_base(self):
        """Удаляем все данные из базы данных"""
        with self.db:
            self.cursor.execute("""DELETE FROM iz_news""")

    def get_article_category(self, news: BeautifulSoup) -> str:
        """Получаем рубрику новости"""
        return news.find('a').text

    def get_article_summary(self, news: BeautifulSoup) -> str:
        """Получаем краткое описание новости"""
        return news.find('div', 'node__cart__item__inside__info__title small-title-style1').text.strip()

    def get_article_image_url(self, news: BeautifulSoup) -> str:
        """Получаем url изображения новости"""
        return 'https://' + news.find('img').get('data-src')[2:]

    def get_article_link(self, news: BeautifulSoup) -> str:
        """Получаем ссылку на новость, на ресурсе источника новостей"""
        first_part_url = self.SOURCE_MAIN_URL.rpartition('/')[0]
        return first_part_url + news.find('a', class_='node__cart__item__inside').get('href')

    def get_article_datetime(self, news: BeautifulSoup) -> str:
        """Получаем дату и время новости"""
        datetime_text = news.time.get('datetime')
        for symbol in '-ZT:':
            while symbol in datetime_text:
                datetime_text = datetime_text.replace(symbol, ' ')
        return datetime_text.strip()

    def caption_message(self, news: dict) -> str:
        """Создаём подпись для изображения поста"""
        category = news['category']
        summary = news['summary']
        link_news = news['link']
        row_list_message = [f'<b>{category}</b>',
                            summary,
                            f'подробнее {hlink(" здесь ", link_news)}',
                            f'Источник: {hlink(self.SOURCE, self.SOURCE_MAIN_URL)}',
                            self.get_footer(),
                            ]
        return '\n\n'.join(row_list_message)

    def get_footer(self):
        """Создаём footer для поста"""
        return f'#{self.HASHTAG} {hlink("Подписаться", "https://t.me/+pxWMeyikCNdjOGNi")}'

# TODO абстрактный класс
