from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

# кнопки клавиатуры чат-бота
reply_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text='Показать все рубрики'),
    ],
    [
        KeyboardButton(text='Удалить все рубрики'),
        KeyboardButton(text='Добавить все рубрики'),
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
        KeyboardButton(text='🏋🏽'),
        KeyboardButton(text='🔭'),
        KeyboardButton(text='⛱'),
    ],
], resize_keyboard=True)
