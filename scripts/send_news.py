import asyncio

# from news_sources.iz_news_source import IZNewsSource
# import aiohttp
from aiogram import Bot, Dispatcher
from aiogram.types import Message
import os
import logging
from dotenv import load_dotenv

load_dotenv()


async def start_bot(bot: Bot):
    await bot.send_message(342786961, text='Бот запущен!')


async def stop_bot(bot: Bot):
    await bot.send_message(342786961, text='Бот остановлен!')


async def get_start(message: Message, bot: Bot):
    await bot.send_message(message.from_user.id, f'Привет {message.from_user.first_name}. Рад тебя видеть!')
    await message.answer(f'Привет {message.from_user.first_name}. Рад тебя видеть!')
    await message.reply(f'Привет {message.from_user.first_name}. Рад тебя видеть!')


async def start():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - [%(levelname)s] - %(name)s - "
               "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
    )
    bot = Bot(token=os.getenv('API_TOKEN'))

    dp = Dispatcher()
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)
    dp.message.register(get_start)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

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
    asyncio.run(start())
