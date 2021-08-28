from shared.instances import dp
from aiogram import types as t
from utils import filters as f


async def sosalka(msg: t.Message):
    '''сосет сообщения'''
    text = msg.text or msg.caption
    if text.startswith('/'):
        return False
    with open('samples.txt', 'a+') as file:
        file.write(text.replace('§', '').lower() + '§')
    return False


@dp.message_handler(f.message.is_chat, f.message.has_text, sosalka, content_types=[t.ContentType.ANY])
async def НАХУЯ_ПРАВДА_Я_НЕ_ЗНАЮ_ЗАЧЕМ_ЭТА_ФУНКЦИЯ_НУЖНА():
    print('NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER ')
    return 'я могу сюда любую хуйню написать, все равно в фильтре фолз =)))))))))))))))))00'
