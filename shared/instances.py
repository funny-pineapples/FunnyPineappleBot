from os.path import exists

from aiogram import Bot, Dispatcher
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from shared.settings import Chats, Settings

settings = Settings()
chats = Chats("data/config.json")
if not exists("data/config.json"):
    chats.save()
chats.load()

bot = Bot(token=settings.token)
dp = Dispatcher(bot)

engine = create_engine("sqlite:///data/database.sqlite")
session = sessionmaker(engine, Session)
