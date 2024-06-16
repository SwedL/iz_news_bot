from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# reply_keyboard = ReplyKeyboardMarkup(keyboard=[
#     [
#         KeyboardButton(text='Очистить рубрики'),
#     ],
#     [
#         KeyboardButton(text='Мир'),
#         KeyboardButton(text='Общество'),
#         KeyboardButton(text='ЧП'),
#         KeyboardButton(text='Здоровье'),
#         KeyboardButton(text='Армия'),
#
#     ],
#     [
#         KeyboardButton(text='Экономика'),
#         KeyboardButton(text='Политика'),
#         KeyboardButton(text='Недвижимость'),
#         KeyboardButton(text='Авто'),
#         KeyboardButton(text='Культура'),
#
#     ],
# [
#         KeyboardButton(text='Пресс-Релизы'),
#         KeyboardButton(text='Спорт'),
#         KeyboardButton(text='Наука и техника'),
#         KeyboardButton(text='Туризм'),
#     ],
# ], resize_keyboard=True)

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

