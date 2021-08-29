import mc
from shared.instances import dp
from aiogram import types as t
from utils import filters as f


@dp.message_handler(f.message.chance(10), f.message.is_chat, content_types=[t.ContentType.ANY])
async def срать_сообщение_с_шансом(msg: t.Message):
    await сгенерировать_хуету(msg)


@dp.message_handler(f.message.is_chat, commands=['gen'])
async def сгенерировать_хуету(msg: t.Message):
    samples = mc.util.load_txt_samples('samples.txt', separator='§')
    await msg.answer(mc.StringGenerator(samples=samples).generate_string())
