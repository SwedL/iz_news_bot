import unittest
import aiofiles
from unittest.mock import patch
from core.news_sources.iz_news_source import IZNewsSource
from pathlib import Path
from bs4 import BeautifulSoup


class IZNewsSourceTestCase(unittest.IsolatedAsyncioTestCase):
    """Тест методов класса IZNewsSource"""

    def setUp(self):
        print('Running setUp')
        self.source = IZNewsSource()
        self.source.DATABASE = Path(__file__).parent.parent.parent / 'iz_news_test.db'
        self.source.create_database()
        print('finish setUp')

    def tearDown(self):
        print('Running tearDown')
        self.source.clear_data_base()

    async def test_get_news(self):
        await self.source.get_parsed_source()  # получаем содержимое страницы новостей
        self.source.get_processed_news_list()  # формируем список обработанных новостей
        self.source.sorted_processed_news_list()  # сортируем новости согласно времени их выхода
        self.source.filter_category()  # фильтруем новости, согласно списку выбранных рубрик в чат-боте
        self.source.saving_news_to_database()  # сохраняем свежие новости в БД для последующего определения старых новостей
        proceed_news_list = self.source.list_processed_news
        first_proceed_news = proceed_news_list[0]

        # проверяем количество полученных новостей со страницы новостного источника
        self.assertEqual(len(proceed_news_list), 16)

        # проверяем ключи словаря первой новости
        self.assertEqual(
            list(first_proceed_news),
            ['category', 'summary', 'image_url', 'link', 'datetime']
        )


if __name__ == '__main__':
    unittest.main()
