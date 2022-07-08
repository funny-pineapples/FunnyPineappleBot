from aiogram import types as t

from shared.instances import dp
from utils import filters as f


@dp.my_chat_member_handler(f.user.add_member)
async def создатьтемплейты(upd: t.ChatMemberUpdated):
    open(f"data/{upd.chat.id}", "w").close()
