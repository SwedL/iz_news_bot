from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

reply_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text='Очистить рубрики'),
    ],
    [
        KeyboardButton(text='Мир'),
        KeyboardButton(text='Общество'),
        KeyboardButton(text='Происшествия'),
        KeyboardButton(text='💊'),
        KeyboardButton(text='Армия'),

    ],
    [
        KeyboardButton(text='Экономика'),
        KeyboardButton(text='Политика'),
        KeyboardButton(text='Недвижимость'),
        KeyboardButton(text='Авто'),
        KeyboardButton(text='Культура'),

    ],
], resize_keyboard=True)


