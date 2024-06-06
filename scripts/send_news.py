import requests
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


def main():
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
        print(f'Новость {caption} была уже отправлена')
        time.sleep(5)


if __name__ == "__main__":
    main()
