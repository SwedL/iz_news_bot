import asyncio

from aiogram import Bot, Dispatcher
from aiogram.types import Message, ContentType
from core.handlers.basic import get_start
from core.settings import settings
import os
import logging
from dotenv import load_dotenv
from aiogram.filters import Command
from aiogram import F
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from core.handlers import apsched
from datetime import datetime, timedelta
from core.news_sources.iz_news_source import IZNewsSource
from core.utils.commands import set_commands

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(name)s - "
           "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
)


class IzNews:
    def __init__(self):
        self.bot = Bot(token=settings.bots.bot_token)
        self.chat_id = settings.bots.admin_id
        self.source = IZNewsSource()

    async def start_bot(self):
        await set_commands(self.bot)
        await self.bot.send_message(settings.bots.admin_id, text='Бот запущен!')

    async def stop_bot(self):
        await self.bot.send_message(settings.bots.admin_id, text='Бот остановлен!')

    async def start(self):
        dp = Dispatcher()
        scheduler = AsyncIOScheduler()

        dp.startup.register(self.start_bot)
        dp.shutdown.register(self.stop_bot)
        dp.message.register(get_start, Command(commands=['start', 'run']))

        # Определяем периодические задачи для бота
        scheduler.add_job(apsched.send_message_time, trigger='date', run_date=datetime.now() + timedelta(seconds=5),
                          kwargs={'bot': self.bot, 'chat_id': self.chat_id, 'source': self.source})
        scheduler.add_job(apsched.send_message_interval, trigger='interval', seconds=30,
                          kwargs={'bot': self.bot, 'chat_id': self.chat_id, 'source': self.source})
        scheduler.start()

        try:
            await dp.start_polling(self.bot)
        finally:
            await self.bot.session.close()


if __name__ == "__main__":
    iz = IzNews()
    asyncio.run(iz.start())
    # try:
    #     asyncio.run(iz.start())
    # except:
    #     pass

