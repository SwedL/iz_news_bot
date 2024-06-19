from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


reply_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text='Удалить все рубрики'),
        KeyboardButton(text='Показать все рубрики'),
    ],
    [
        KeyboardButton(text='🌍'),
        KeyboardButton(text='👨‍👩‍👧‍👦'),
        KeyboardButton(text='🚔'),
        KeyboardButton(text='💊'),
        KeyboardButton(text='🪖'),

    ],
    [
        KeyboardButton(text='💵'),
        KeyboardButton(text='💼'),
        KeyboardButton(text='🏙'),
        KeyboardButton(text='🚗'),
        KeyboardButton(text='🎼'),

    ],
[
        KeyboardButton(text='📰'),
        KeyboardButton(text='⚽️'),
        KeyboardButton(text='🔭'),
        KeyboardButton(text='⛱'),
    ],
], resize_keyboard=True)

m = {
    'Мир': '🌍', 'Общество': '👨‍👩‍👧‍👦', 'ЧП': '🚔', 'Здоровье': '💊', 'Армия': '🪖',
    'Экономика': '💵', 'Политика': '💼', 'Недвижимость': '🏙', 'Авто': '🚗', 'Культура': '🎼',
    'Пресс-Релизы': '📰', 'Спорт': '⚽️', 'Наука и техника': '🔭', 'Туризм': '⛱',
}

