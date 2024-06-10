from aiogram import Bot
from aiogram.types import Message
from core.keyboards.reply import reply_keyboard


async def get_start(message: Message, bot: Bot):

    await message.answer(f'Привет {message.from_user.first_name}. Рад тебя видеть!',
                         reply_markup=reply_keyboard)


async def get_photo(message: Message, bot: Bot):
    await message.answer('Отлично ты отправил фото! Сохраню его себе')
    file = await bot.get_file(message.photo[-1].file_id)
    await bot.download_file(file.file_path, 'photo.jpg')
