import unittest
from core.news_sources.iz_news_source import IZNewsSource
from pathlib import Path


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
        await self.source.get_news()
        self.source.saving_news_to_database()
        proceed_news_list = self.source.list_processed_news
        first_proceed_news = proceed_news_list[0]

        self.assertEqual(len(proceed_news_list), 16)
        self.assertEqual(
            list(first_proceed_news),
            ['category', 'summary', 'image_url', 'link', 'datetime']
        )


if __name__ == '__main__':
    unittest.main()
