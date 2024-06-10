from dataclasses import dataclass
from dotenv import load_dotenv
import os

load_dotenv()


@dataclass
class Bots:
    bot_token: str
    admin_id: int


@dataclass
class Settings:
    bots: Bots


def get_settings():
    return Settings(
        bots=Bots(
            bot_token=os.getenv('API_TOKEN'),
            admin_id=int(os.getenv('CHANNEL_ID')),
        )
    )


settings = get_settings()
