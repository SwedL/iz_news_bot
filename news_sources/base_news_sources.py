import sqlite3
from typing import Dict, List
from abc import ABC, abstractmethod
from telebot import formatting
import requests
from pathlib import Path
from bs4 import BeautifulSoup
from news_sources.types import NewsData
from fake_useragent import FakeUserAgent


# def read_file():
#     with open('./../iz_news_text', 'r', encoding='utf-8') as f:
#         input_data = f.read()
#         soup = BeautifulSoup(input_data, 'lxml')
#     return soup
# self.parsed_source = read_file()


class BaseNewsSource(ABC):
    SOURCE = ''
    DATABASE = Path(__file__).parent.parent / 'news.db'

    def __init__(self, url: str):
        self.list_processed_news = []
        self.db = sqlite3.connect(self.DATABASE)
        self.cursor = self.db.cursor()
        self._create_database()
        self.parsed_source = BeautifulSoup(
            requests.get(
                url=url,
                headers=self._get_headers(),
            ).text,
            features='html.parser'
        )

    def get_news(self):
        raw_news = self._get_raw_today_news()
        self._raw_news_list(raw_news=raw_news)
        self._filter_actual_news()
        self._sorted_news_list()

    @staticmethod
    def _get_headers() -> Dict[str, str]:
        ua = FakeUserAgent()
        return {
            'User-Agent': ua.random
        }

    @abstractmethod
    def _get_footer(self):
        pass

    def _create_database(self):
        with self.db:
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS news (
            category text,
            summary text,
            image_url text,
            link text,
            datetime text
            )""")

    @abstractmethod
    def _get_raw_today_news(self) -> List[BeautifulSoup]:
        pass

    @abstractmethod
    def _raw_news_list(self, raw_news: List[BeautifulSoup]) -> None:
        pass

    @abstractmethod
    def _sorted_news_list(self) -> None:
        pass

    @abstractmethod
    def _saving_news_to_database(self) -> None:
        pass

    @abstractmethod
    def _filter_actual_news(self) -> None:
        pass

    @abstractmethod
    def _get_article_category(self, news: BeautifulSoup) -> str:
        pass

    @abstractmethod
    def _get_article_summary(self, news: BeautifulSoup) -> str:
        pass

    @abstractmethod
    def _get_article_image_url(self, news: BeautifulSoup) -> str:
        pass

    @abstractmethod
    def _get_article_link(self, news: BeautifulSoup) -> str:
        pass

    @abstractmethod
    def _get_article_datetime(self, news: BeautifulSoup) -> str:
        pass



