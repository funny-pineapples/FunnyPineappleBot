from ast import literal_eval
from copy import deepcopy
from logging import info
from typing import Any, get_args

from aiogram import types as t
from pydantic import BaseModel, ValidationError

from shared.database import Message
from shared.instances import config, dp, session
from shared.settings import Config
from utils import filters as f


@dp.message_handler(f.user.is_admin, commands=["void"])
async def void_command(msg: t.Message) -> None:
    if msg.get_args() == "Я знаю что делаю":
        with session.begin() as s:
            s.query(Message).filter(Message.chat_id == msg.chat.id).delete()
        await msg.answer("Лоботомия проведена успешно")
    else:
        await msg.answer(
            "Напишите <code>/void Я знаю что делаю</code>",
            parse_mode=t.ParseMode.HTML,
        )


@dp.message_handler(f.message.is_chat, f.user.is_admin, commands=["config"])
async def settings_command(msg: t.Message) -> None:
    def get_fields(config: BaseModel, level: int = 1) -> str:
        text = ""
        for name in config.__fields__:
            value = getattr(config, name)
            if isinstance(value, BaseModel):
                text += f"\n{' '*level*4}<code>{name}.</code>"
                text += get_fields(value, level + 1)
            else:
                text += f"\n{' '*level*4}<code>{name}</code> = {value!r}"
        return text

    args = msg.get_args().split()
    chat_config = deepcopy(config.get_config(msg.chat.id))
    try:
        if len(args) == 0:
            text = f"<code>/config</code>{get_fields(chat_config)}\n\n"
            await msg.reply(text, parse_mode=t.ParseMode.HTML)
        else:
            conf = chat_config
            *path, field = args[0].split(".")
            for f in path:
                conf = getattr(conf, f)
                if not isinstance(conf, BaseModel):
                    raise KeyError()

            if len(args) == 2:
                if isinstance(getattr(conf, field), BaseModel):
                    raise KeyError()
                value = args[1]
                setattr(conf, field, literal_eval(value))

                config.set_config(msg.chat.id, Config.parse_obj(chat_config.dict()))
                config.save("data/config.json")

                await msg.reply(
                    f"<code>/config {args[0]}</code> = {getattr(conf, field)!r}",
                    parse_mode=t.ParseMode.HTML,
                )
            else:
                field_info = conf.__fields__[field].field_info
                await msg.reply(
                    f"<code>/config {args[0]}</code> = {getattr(conf, field)!r}\n{field_info.description}",
                    parse_mode=t.ParseMode.HTML,
                )
    except (ValidationError, ValueError, SyntaxError):
        await msg.reply("Неверное значение")
    except (KeyError, AttributeError):
        await msg.reply("Параметр не найден")
