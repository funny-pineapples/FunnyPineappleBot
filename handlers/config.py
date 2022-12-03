from json import JSONDecodeError, dumps, loads

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
        for field_name in config.__fields__:
            field = getattr(config, field_name)
            field_info = config.__fields__[field_name].field_info

            text += "\n" + "  " * level
            if isinstance(field, BaseModel):
                text += f"<code>{field_name}.</code> {field_info.description}"
                text += get_fields(field, level + 1)
            else:
                text += f"<code>{field_name}</code> = {dumps(field)}"
        return text

    def get_field(config: BaseModel, path: list[str]) -> str:
        text = ""
        for field_name in path:
            assert (
                isinstance(config, BaseModel) and f in config.__fields__
            ), "Параметр не найден"
            field_info = config.__fields__[field_name].field_info
            config = getattr(config, field_name)

        text += field_info.description
        text += "\n\n"
        if isinstance(config, BaseModel):
            text += f"<code>/config {'.'.join(path)}.</code>"
            text += get_fields(config, 1)
        else:
            text += f"<code>/config {'.'.join(path)}</code> {dumps(config)}"
        return text

    def set_filed(config: BaseModel, path: list[str], value: str) -> str:
        text = ""
        field_name = path[-1]

        for f in path[:-1]:
            assert (
                isinstance(config, BaseModel) and f in config.__fields__
            ), "Параметр не найден"
            config = getattr(config, f)

        assert not isinstance(
            getattr(config, field_name), BaseModel
        ), "Нельзя установить значение для группы параметров"

        setattr(config, field_name, loads(value))

        text += (
            f"Значение <code>{'.'.join(path)}</code> установлено на <code>{value}</code>"
        )

        return text

    chat_config = config.get_config(msg.chat.id)
    args = msg.get_args().split()
    if len(args) == 0:
        text = f"<code>/config</code>{get_fields(chat_config)}"
    elif len(args) == 1:
        text = get_field(chat_config, args[0].split("."))
    elif len(args) == 2:
        try:
            text = set_filed(chat_config, args[0].split("."), args[1])
            config.set_config(msg.chat.id, Config.parse_obj(chat_config.dict()))
            config.save("data/config.json")
        except (JSONDecodeError, ValidationError):
            text = "Неверное значение"
    else:
        text = "Слишком много аргументов"
    await msg.answer(text, parse_mode=t.ParseMode.HTML)
