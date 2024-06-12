import asyncio

from aiogram import Bot, Dispatcher
from aiogram.types import Message, ContentType
from core.handlers.basic import get_start, get_photo
from core.settings import settings
import os
import logging
from dotenv import load_dotenv
from aiogram.filters import Command
from aiogram import F
from news_sources.iz_news_source import IZNewsSource

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(name)s - "
           "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
)


class IzNews:
    def __init__(self):
        self.bot = Bot(token=settings.bots.bot_token)
        self.source = IZNewsSource()

    async def start_bot(self):
        await self.bot.send_message(settings.bots.admin_id, text='Бот запущен!')

    async def stop_bot(self):
        await self.bot.send_message(settings.bots.admin_id, text='Бот остановлен!')

    async def start(self):
        dp = Dispatcher()
        dp.startup.register(self.start_bot)
        dp.shutdown.register(self.stop_bot)
        dp.message.register(get_photo, F.photo)
        dp.message.register(get_start, Command(commands=['start', 'run']))

        try:
            await dp.start_polling(self.bot)
        finally:
            await self.bot.session.close()

        chat_id = os.getenv('CHANNEL_ID')
        # source = IZNewsSource()
        # source.get_news()
        # news_to_post = source.list_processed_news

        # for news in news_to_post:
        #     photo = requests.get(news.get('image_url', source.DEFAULT_IMAGE_URL)).content
        #     caption = source.caption_message(news)
        #
        #     bot.send_photo(
        #         chat_id=chat_id,
        #         photo=photo,
        #         caption=caption,
        #     )
        #     print(f'Новость {news["summary"]} была отправлена')
        #     time.sleep(5)


if __name__ == "__main__":
    iz = IzNews()
    try:
        asyncio.run(iz.start())
    except:
        pass

