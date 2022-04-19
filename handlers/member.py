from asyncio import sleep

from aiogram import types as t

from shared.instances import bot, dp
from utils import filters as f

unmute = t.ChatPermissions(*[True] * 8)
mute = t.ChatPermissions(*[False] * 8)


@dp.chat_member_handler(f.user.add_member)
async def запрашиваем_пропуск(upd: t.ChatMemberUpdated):
    pass_user_markup = t.InlineKeyboardMarkup().add(
        t.InlineKeyboardButton(
            "Да", callback_data=f"pass_user@{upd.new_chat_member.user.id}"
        ),
        t.InlineKeyboardButton(
            "Нет", callback_data=f"kick_user@{upd.new_chat_member.user.id}"
        ),
    )
    await upd.chat.restrict(upd.new_chat_member.user.id, mute)
    await bot.send_message(
        upd.chat.id,
        f'Это наш <a href="tg://user?id={upd.new_chat_member.user.id}">чел</a> ?',
        parse_mode=t.ParseMode.HTML,
        reply_markup=pass_user_markup,
    )


@dp.callback_query_handler(
    f.message.is_chat, lambda clb: clb.data.split("@")[0] == "pass_user"
)
async def пропустить(clb: t.CallbackQuery):
    member = await clb.message.chat.get_member(clb.from_user.id)
    if not member.is_chat_admin():
        await clb.answer("Ты не админ")
        return
    else:
        await clb.message.chat.restrict(int(clb.data.split("@")[1]), unmute)

    await clb.message.delete()
    await clb.message.answer(
        f'<a href="tg://user?id={int(clb.data.split("@")[1])}">Ананасер</a> добро пожаловать в чат для <a href="tg://user?id={clb.from_user.id}">крутых</a>',
        parse_mode=t.ParseMode.HTML,
    )


@dp.callback_query_handler(
    f.message.is_chat, lambda clb: clb.data.split("@")[0] == "kick_user"
)
async def выкинуть(clb: t.CallbackQuery):
    member = await clb.message.chat.get_member(clb.from_user.id)
    await clb.message.delete()
    await clb.message.answer(
        f'Эта группа для <a href="tg://user?id={clb.from_user.id}">крутых</a>',
        parse_mode=t.ParseMode.HTML,
    )

    await sleep(3)

    if not member.is_chat_admin():
        await clb.answer("Ты не админ")
        return
    else:
        await clb.message.chat.unban(int(clb.data.split("@")[1]), False)
