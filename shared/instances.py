from aiogram import Bot, Dispatcher

from shared.config import token

bot = Bot(token=token)
dp = Dispatcher(bot)
