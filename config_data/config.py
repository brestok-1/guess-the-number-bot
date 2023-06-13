from dataclasses import dataclass
from dotenv import load_dotenv
import os


@dataclass
class TgBot:
    token: str


@dataclass
class Config:
    tg_bot: TgBot


def load_config(path: str | None = None) -> Config:
    load_dotenv()
    return Config(tg_bot=TgBot(token=os.getenv('BOT_TOKEN')))


ATTEMPTS = 5
