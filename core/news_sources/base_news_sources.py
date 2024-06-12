from typing import Dict, List
from abc import ABC, abstractmethod
import requests
from bs4 import BeautifulSoup
from fake_useragent import FakeUserAgent


class BaseNewsSource(ABC):
    SOURCE = ''

    def __init__(self, url: str):
        self.list_processed_news = []
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



