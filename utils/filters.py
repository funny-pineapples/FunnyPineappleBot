from __future__ import annotations

from random import randint

from aiogram import filters as f
from aiogram import types as t

from shared.instances import config


class message:
    is_chat = f.ChatTypeFilter((t.ChatType.GROUP, t.ChatType.SUPERGROUP))

    @staticmethod
    def chance(msg: t.Message) -> bool:
        return config.get_config(msg.chat.id).gen.chance >= randint(1, 100)


class user:
    @staticmethod
    async def is_admin(msg: t.Message) -> bool:
        if not await message.is_chat.check(msg):
            return True
        member = await msg.chat.get_member(msg.from_user.id)
        if not member.is_chat_admin():
            await msg.answer(
                "Вы не администратор. Данное действие будет занесено в журнал."
            )
            return False
        return True
