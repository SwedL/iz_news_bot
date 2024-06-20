import asyncio

from aiogram import Bot

from core.news_sources.iz_news_source import IZNewsSource


async def send_message_interval(bot: Bot, chat_id: int, source: IZNewsSource):
    """Отправляет сообщения, с интервалом в 5 минут"""
    await send_received_news(bot, chat_id, source)


async def send_received_news(bot: Bot, chat_id: int, source: IZNewsSource):
    """Получает последние новости с новостного ресурса и отправляет в телеграм-канал"""
    await source.get_parsed_source()  # получаем содержимое страницы новостей
    source.get_processed_news_list()  # формируем список обработанных новостей
    source.sorted_processed_news_list()  # сортируем новости согласно времени их выхода
    source.filter_category()  # фильтруем новости, согласно списку выбранных рубрик в чат-боте
    source.saving_news_to_database()  # сохраняем свежие новости в БД для последующего определения старых новостей

    for news in source.list_processed_news:
        caption = source.caption_message(news)

        await bot.send_photo(
            chat_id=chat_id,
            photo=news.get('image_url', source.DEFAULT_IMAGE_URL),
            caption=caption,
            parse_mode='html',
        )
        print(f'Новость >>{news["summary"]}<< была отправлена')

        await asyncio.sleep(5)


async def delete_old_news(source: IZNewsSource):
    """Удаляет старые новости из базы данных"""
    source.delete_old_news_from_data_base()
    await asyncio.sleep(0.5)
