from aiogram import Bot, Dispatcher
from config import token

print(token)
bot = Bot(token=token)
dp = Dispatcher(bot)
gen_chance = 10
