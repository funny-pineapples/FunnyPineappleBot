from shared.instances import dp
from aiogram import types as t
from utils import filters as f


@dp.my_chat_member_handler(f.user.add_member)
async def pososi(upd: t.ChatMemberUpdated):
    if upd.chat.id not in (-1001444484622, -1001197098429):
        await upd.bot.send_message(upd.chat.id, 'https://www.youtube.com/watch?v=xdDhmagsXrc')
        await upd.chat.leave()
