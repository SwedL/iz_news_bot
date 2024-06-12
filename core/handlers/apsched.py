from aiogram import Bot


async def send_message_time(bot: Bot, chat_id: int):
    await bot.send_message(chat_id, 'Это сообщение будет отправляться через 10 секунд после старта бота')


# async def send_message_cron(bot: Bot, chat_id: int):
#     await bot.send_message(chat_id, 'Это сообщение будет отправляться ежедневно в указанное время')


async def send_message_interval(bot: Bot, chat_id: int):
    await bot.send_message(chat_id, 'Это сообщение будет отправляться с интервалом в 5 минут')
