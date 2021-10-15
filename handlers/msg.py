from shared.instances import dp
from aiogram import types as t
from utils import filters as f


async def сосалка(msg: t.Message):
    text = msg.text or msg.caption
    if text.startswith('/'):
        return False
    with open('samples.txt', 'a+') as file:
        file.write(text.lower().replace('§', '') + '§')
    return False


@dp.message_handler(f.message.is_chat, f.message.has_text, сосалка, content_types=[t.ContentType.ANY])
async def ХУЙ():
    pass
