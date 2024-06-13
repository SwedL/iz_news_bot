from aiogram import Bot
from aiogram.types import Message
from core.keyboards.reply import reply_keyboard
from core.news_sources.iz_news_source import IZNewsSource


async def get_start(message: Message, bot: Bot):
    await message.answer(f'Привет {message.from_user.first_name}. Рад тебя видеть!',
                         reply_markup=reply_keyboard)


async def handler_messages(message: Message, bot: Bot):
    await message.answer(f'{message.text}  dwdwqdwd')
