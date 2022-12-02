from logging import info

from aiogram import types as t
from aiogram.dispatcher.middlewares import BaseMiddleware

from shared.database import Message
from shared.instances import session


class MessageMiddleware(BaseMiddleware):
    async def on_pre_process_message(self, msg: t.Message, data: dict) -> None:
        text = msg.text or msg.caption
        if text is not None and not text.startswith("/"):
            with session.begin() as s:
                s.add(
                    Message(
                        chat_id=msg.chat.id,
                        message_id=msg.message_id,
                        message=text,
                    )
                )
