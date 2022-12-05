from aiogram import types as t

from shared.instances import chats, dp
from shared.samples import samples
from utils import filters as f


@dp.message_handler(commands=["gen"])
async def gen_command(msg: t.Message) -> None:
    if chats.get(msg.chat.id).gen.delete_command:
        await msg.delete()
    await msg.answer(samples.get(msg.chat.id).generate())


@dp.message_handler(
    f.message.is_chat,
    f.message.chance,
    content_types=[t.ContentType.ANY],
)
async def chance_message(msg: t.Message) -> None:
    if chats.get(msg.chat.id).gen.reply:
        await msg.reply(samples.get(msg.chat.id).generate())
    else:
        await msg.answer(samples.get(msg.chat.id).generate())
