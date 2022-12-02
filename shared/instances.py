from os.path import exists

from aiogram import Bot, Dispatcher
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from shared.settings import Chats, Settings

settings = Settings()
config = Chats()
if not exists("data/config.json"):
    config.save("data/config.json")
config.load("data/config.json")

bot = Bot(token=settings.token)
dp = Dispatcher(bot)

engine = create_engine("sqlite:///data/database.sqlite")
session = sessionmaker(engine, Session)
