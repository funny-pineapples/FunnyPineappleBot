import random

import mc
from aiogram import types as t

from shared.database import Message
from shared.instances import bot, config, dp, session
from utils import filters as f


def get_text(chat_id: int) -> str:
    with session() as s:
        samples = [
            m.tuple()[0]
            for m in s.query(Message.message).filter(Message.chat_id == chat_id).all()
        ]

    assert (
        len(samples) != 0
    ), "Нету данных на основе которых можно сгенерировать сообщение"

    generator = mc.PhraseGenerator(samples)
    gen_config = config.get_config(chat_id).gen
    validators = []

    if gen_config.max_word_count is not None or gen_config.min_word_count is not None:
        validators.append(
            mc.builtin.validators.words_count(
                minimal=gen_config.min_word_count,
                maximal=gen_config.max_word_count,
            )
        )

    while True:
        message = generator.generate_phrase_or_none(1, validators=validators)
        if message is not None:
            return message


@dp.message_handler(commands=["gen"])
async def gen_command(msg: t.Message) -> None:
    if config.get_config(msg.chat.id).gen.delete_command:
        await msg.delete()
    await msg.answer(get_text(msg.chat.id))


@dp.message_handler(commands=["del"])
async def del_command(msg: t.Message) -> None:
    await msg.delete()

    if msg.reply_to_message:
        if msg.reply_to_message.from_user.id == bot.id:
            await msg.reply_to_message.delete()
        else:
            await msg.reply("Можно удалять только сообщения бота")
    else:
        await msg.reply("Вы не ответили на сообщение")


@dp.message_handler(
    f.message.is_chat,
    f.message.chance,
    content_types=[t.ContentType.ANY],
)
async def chance_message(msg: t.Message) -> None:
    if config.get_config(msg.chat.id).gen.reply:
        await msg.reply(get_text(msg.chat.id))
    else:
        await msg.answer(get_text(msg.chat.id))
