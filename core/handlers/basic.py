import asyncio

from aiogram.types import Message

from core.keyboards.reply import reply_keyboard
from core.news_sources.iz_news_source import IZNewsSource

category_news_dict = {'🌍': 'Мир', '👨‍👩‍👧‍👦': 'Общество', '🚔': 'Происшествия', '💊': 'Здоровье', '🪖': 'Армия',
                      '💵': 'Экономика', '💼': 'Политика', '🏙': 'Недвижимость', '🚗': 'Авто', '🎼': 'Культура',
                      '📰': 'Пресс-релизы', '🏋🏽': 'Спорт', '🔭': 'Наука и техника', '⛱': 'Туризм'}


async def get_start(message: Message):
    """При получении сообщения start - приветствует в сообщении и обновляет клавиатуру чат-бота"""
    await message.answer(f'Привет {message.from_user.first_name}. Рад тебя видеть!',
                         reply_markup=reply_keyboard)


async def handler_messages(message: Message, source: IZNewsSource):
    """Проверяет полученное сообщение и если оно находится в словаре рубрик, добавляет/удаляет
    соответствующую рубрику из списка рубрик получаемых новостей"""

    news_category_filter = source.news_category_filter  # получаем список рубрик новостей
    message_text = message.text

    if message_text == 'Показать все рубрики':
        all_select_category = '\n'.join(news_category_filter)
        await message.answer(f'Список выбранных рубрик:\n{all_select_category}')

    if message_text == 'Удалить все рубрики':
        source.news_category_filter.clear()
        await message.answer('Все рубрики удалены')

    if message_text == 'Добавить все рубрики':
        source.news_category_filter = list(category_news_dict.values())
        await message.answer('Все рубрики были добавлены')

    if len(message_text.split()) == 1 and message_text in category_news_dict.keys():
        selected_category = category_news_dict.get(message_text, None)
        if selected_category in news_category_filter:
            news_category_filter.remove(selected_category)
            await message.answer(f'--- рубрика {selected_category}')
        else:
            news_category_filter.append(selected_category)
            await message.answer(f'+++ рубрика {selected_category}')

        if news_category_filter:
            await message.answer('\n'.join(news_category_filter))
        else:
            await message.answer('Список рубрик пуст')

    await asyncio.sleep(0)
