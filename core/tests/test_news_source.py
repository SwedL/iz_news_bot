import unittest
from itertools import pairwise
from pathlib import Path

from bs4 import BeautifulSoup

from ..news_sources.iz_news_source import IZNewsSource


class IZNewsSourceTestCase(unittest.IsolatedAsyncioTestCase):
    """Тест методов класса IZNewsSource"""

    @classmethod
    def setUpClass(cls):
        # Вызывается один раз для всего класса
        print('Running setUp')
        cls.source = IZNewsSource()
        cls.source.DATABASE = Path(__file__).parent.parent.parent / 'iz_news_test.db'
        cls.source.create_database()
        print('Finish setUp')

    async def test_get_news(self):
        """Тестирование получения контента страницы с новостного ресурса"""
        self.assertIs(self.source.parsed_source, None)
        await self.source.get_parsed_source()  # получаем контент страницы новостей
        self.assertIsInstance(self.source.parsed_source, BeautifulSoup)

    def test_get_processed_news_list(self):
        """Тестирование получения списка обработанных новостей"""
        self.assertIsNot(self.source.list_processed_news, [])
        self.source.get_processed_news_list()  # формируем список обработанных новостей
        proceed_news_list = self.source.list_processed_news
        first_proceed_news = proceed_news_list[0]

        self.assertIsNotNone(self.source.list_processed_news)  # проверяем наличие списка обработанных новостей
        self.assertEqual(len(proceed_news_list), 16)  # проверяем количество обработанных новостей
        # проверяем ключи словаря первой новости
        self.assertEqual(list(first_proceed_news), ['category', 'summary', 'image_url', 'link', 'datetime'])

    def test_sorting_processed_news_list(self):
        """Тестирование функции сортировки новостей относительно даты новости"""
        self.source.sorting_processed_news_list()  # сортируем новости согласно времени их выхода
        sorted_processed_news_list = self.source.list_processed_news

        pairwise_iter = pairwise(sorted_processed_news_list)
        check_sorting = all(map(lambda n: n[0]['datetime'] <= n[1]['datetime'], pairwise_iter))
        self.source.filter_category()  # фильтруем новости, согласно списку выбранных рубрик в чат-боте

        self.assertTrue(check_sorting)  # проверяем что новости отсортированы согласно дате

    def test_saving_news_to_database(self):
        """Тестирование функции сохранения новостей в базу данных"""
        self.source.saving_news_to_database()  # сохр. свежие новости в БД для последующего определения старых новостей
        with self.source.db:
            self.source.cursor.execute('SELECT * FROM iz_news')
            news_in_database = self.source.cursor.fetchall()

        self.assertEqual(len(news_in_database), 16)

    @classmethod
    def tearDownClass(cls):
        # Вызывается один раз после всех тестов
        print('Running tearDown')
        cls.source.clear_data_base()
        print('Finish tearDown')


if __name__ == '__main__':
    unittest.main()
