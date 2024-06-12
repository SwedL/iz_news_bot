from aiogram import Bot
from aiogram.types import Message
from core.keyboards.reply import reply_keyboard


async def get_start(message: Message, bot: Bot):
    await message.answer(f'Привет {message.from_user.first_name}. Рад тебя видеть!',
                         reply_markup=reply_keyboard)
