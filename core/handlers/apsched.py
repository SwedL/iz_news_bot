import asyncio

from aiogram import Bot
from core.news_sources.iz_news_source import IZNewsSource


async def send_message_time(bot: Bot, chat_id: int, source: IZNewsSource):
    """Функция рассылки новостей через 5 секунд после старта бота"""
    await send_received_news(bot, chat_id, source)


async def send_message_interval(bot: Bot, chat_id: int, source: IZNewsSource):
    """Функция рассылки новостей через каждые 5 минут"""
    await send_received_news(bot, chat_id, source)


async def send_received_news(bot: Bot, chat_id: int, source: IZNewsSource):
    """Функция получения новостей с новостного ресурса и их отправка в телеграм-канал"""
    await source.get_news()
    source.filter_category()  # фильтруем новости, согласно списку выбранных рубрик в чат-боте
    source.saving_news_to_database()  # сохраняем свежие новости в БД для последующего определения старых новостей
    news_to_post = source.list_processed_news
    print(len(news_to_post))

    for news in news_to_post:
        caption = source.caption_message(news)

        await bot.send_photo(
            chat_id=chat_id,
            photo=news.get('image_url', source.DEFAULT_IMAGE_URL),
            caption=caption,
            parse_mode='html',
        )
        print(f'Новость {news["summary"]} была отправлена')

        await asyncio.sleep(5)


async def delete_old_news(bot: Bot, chat_id: int, source: IZNewsSource):
    source.delete_old_news_from_data_base()
    await asyncio.sleep(0.5)
