import asyncio
import logging
from datetime import datetime, timedelta

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from core.handlers import apsched
from core.handlers.basic import get_start, handler_messages
from core.middlewares.filter_news_middleware import FilterNewsMiddleware
from core.news_sources.iz_news_source import IZNewsSource
from core.settings import settings
from core.utils.commands import set_commands

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
        self.source.create_database()

    async def run_bot(self):
        """Отправляет соответствующее сообщение в канал чата, при запуске чат-бота"""
        await set_commands(self.bot)
        await self.bot.send_message(settings.bots.admin_id, text='Бот запущен!')

    async def stop_bot(self):
        """Отправляет соответствующее сообщение в канал чата, при остановке чат-бота"""
        await self.bot.send_message(settings.bots.admin_id, text='Бот остановлен!')

    async def main(self):
        dp = Dispatcher()
        scheduler = AsyncIOScheduler()

        dp.message.middleware.register(FilterNewsMiddleware(self.source))  # изменение фильтра новостей
        dp.startup.register(self.run_bot)
        dp.shutdown.register(self.stop_bot)
        dp.message.register(get_start, Command(commands=['start', 'run']))
        dp.message.register(handler_messages, F.text)

        # Периодические задачи для бота
        # задача получает новости с новостного ресурса и размещает их в телеграм-канале, с интервалом в 5 минут
        scheduler.add_job(
            apsched.send_message_interval,
            trigger='interval',
            next_run_time=datetime.now() + timedelta(seconds=5),
            seconds=300,
            kwargs={'bot': self.bot, 'chat_id': self.chat_id, 'source': self.source},
        )
        # задача удаляет старые новости из базы данных 1 раз в день
        scheduler.add_job(
            apsched.delete_old_news,
            trigger='interval',
            seconds=360,
            kwargs={'source': self.source},
        )

        scheduler.start()

        try:
            await dp.start_polling(self.bot)
        finally:
            await self.bot.session.close()


if __name__ == "__main__":
    iz = IzNews()
    try:
        asyncio.run(iz.main())
    except KeyboardInterrupt:
        print('exit')
