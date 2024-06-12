import asyncio

from aiogram import Bot
from core.news_sources.iz_news_source import IZNewsSource


# Рассылка новостей через 5 секунд после старта бота
async def send_message_time(bot: Bot, chat_id: int, source: IZNewsSource):
    await send_received_news(bot, chat_id, source)
    # await bot.send_message(chat_id, 'Это сообщение будет отправляться через 10 секунд после старта бота')


# Рассылка новостей через каждые 5 минут
async def send_message_interval(bot: Bot, chat_id: int, source: IZNewsSource):
    await send_received_news(bot, chat_id, source)
    # await bot.send_message(chat_id, 'Это сообщение будет отправляться с интервалом в 5 минут')


async def send_received_news(bot: Bot, chat_id: int, source: IZNewsSource):
    source.get_news()
    news_to_post = source.list_processed_news
    print(news_to_post)

    for news in news_to_post:
        caption = source.caption_message(news)

        await bot.send_photo(
            chat_id=chat_id,
            photo=news.get('image_url', source.DEFAULT_IMAGE_URL),
            caption=caption,
        )
        print(f'Новость {news["summary"]} была отправлена')

        await asyncio.sleep(5)
