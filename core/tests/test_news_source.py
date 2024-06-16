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
        # with open('iz_news_text', 'r', encoding='utf-8') as f:
        #     self.mock_page = f.read()
        print('finish setUp')

    # def tearDown(self):
    #     print('Running tearDown')
    #     self.source.clear_data_base()
    #
    # async def test_get_news(self):
    #     await self.source.get_news()
    #     self.source.saving_news_to_database()
    #     proceed_news_list = self.source.list_processed_news
    #     first_proceed_news = proceed_news_list[0]
    #
    #     # проверяем количество полученных новостей со страницы новостного источника
    #     self.assertEqual(len(proceed_news_list), 16)
    #
    #     # проверяем ключи словаря первой новости
    #     self.assertEqual(
    #         list(first_proceed_news),
    #         ['category', 'summary', 'image_url', 'link', 'datetime']
    #     )

    @patch.object(IZNewsSource, 'get_parsed_source')
    async def test_get_news_mock(self, mock_parsed_source):
        path = Path(__file__).parent.parent.parent / 'iz_news_text'
        async with aiofiles.open(path, mode='r', encoding='utf-8') as f:
            text = await f.read()
            mock_parsed_source.return_value = BeautifulSoup(text, features='html.parser')
        # print(mock_parsed_source.return_value)
        result = await self.source.get_news()
        print(self.source.parsed_source)
        # print(self.source.list_processed_news)

        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
