from __future__ import annotations

from random import random

from aiogram import types as t, filters as f

from shared import instances as ins


class message:
    is_chat = f.ChatTypeFilter((t.ChatType.GROUP, t.ChatType.SUPERGROUP))
    is_private = f.ChatTypeFilter(t.ChatType.PRIVATE)
    is_reply = f.IsReplyFilter(True)

    @staticmethod
    def chance(msg: t.Message):
        return random() <= (ins.gen_chance / 100)

    @staticmethod
    def has_text(msg: t.Message):
        if msg.text or msg.caption:
            return True


class user:
    @staticmethod
    def add_member(upd: t.ChatMemberUpdated):
        old = upd.old_chat_member
        new = upd.new_chat_member
        return not t.ChatMemberStatus.is_chat_member(old.status) and t.ChatMemberStatus.is_chat_member(new.status)
