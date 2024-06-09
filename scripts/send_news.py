import requests
import telebot
from telebot import TeleBot
import os
from dotenv import load_dotenv
from news_sources.iz_news_source import IZNewsSource
import time

load_dotenv()

bot = TeleBot(
    token=os.getenv('API_TOKEN'),
    parse_mode='html',
    disable_web_page_preview=True,
    )
chat_id = os.getenv('CHANNEL_ID')
source = IZNewsSource()


# # Handle '/start' and '/help'
# @bot.message_handler(commands=['help', 'start'])
# def send_welcome(message):
#     bot.reply_to(message, """\
# Hi there, I am EchoBot.
# I am here to echo your kind words back to you. Just say anything nice and I'll say the exact same thing to you!\
# """)
#
#
# # Handle all other messages with content_type 'text' (content_types defaults to ['text'])
# @bot.message_handler(func=lambda message: True)
# def echo_message(message):
#     bot.reply_to(message, message.text)


def main():
    # bot.infinity_polling()
    source.get_news()
    news_to_post = source.list_processed_news

    for news in news_to_post:
        photo = requests.get(news.get('image_url', source.DEFAULT_IMAGE_URL)).content
        caption = source.caption_message(news)

        bot.send_photo(
            chat_id=chat_id,
            photo=photo,
            caption=caption,
        )
        print(f'Новость {news["summary"]} была отправлена')
        time.sleep(5)


if __name__ == "__main__":
    main()
