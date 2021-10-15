from datetime import datetime, timedelta

from shared.instances import dp, bot
from utils import filters as f
from aiogram import types as t

pin_reply_markup = t.InlineKeyboardMarkup().add(
    t.InlineKeyboardButton("Проверить сейчас", callback_data="chek")
)


@dp.message_handler(f.message.is_chat, commands=["pin"])
async def закрепить_хуету(msg: t.Message):
    await msg.delete()
    if msg.reply_to_message:
        await msg.reply_to_message.reply_poll(
            "Закрепить ?",
            [
                "Да",
                "УДАЛИ НАХУЙ",
                "Нет"
            ],
            close_date=datetime.now() + timedelta(minutes=10),
            reply_markup=pin_reply_markup
        )
    else:
        await msg.answer("Ты умник, ответь на сообщение")


@dp.callback_query_handler(f.message.is_chat, lambda clb: clb.data == "chek")
async def проверить_опрос(clb: t.CallbackQuery):
    poll = clb.message.poll
    msg = clb.message

    if poll.total_voter_count <= 0:
        await clb.answer("Видишь голоса? Вот и я невижу")
    else:
        if not poll.is_closed:
            await bot.stop_poll(msg.chat.id, msg.message_id)
            poll.is_closed = True
        yes = poll.options[0].voter_count
        delete = poll.options[1].voter_count
        win = max(yes, delete)

        if win == yes:
            await msg.reply_to_message.pin()
        elif win == delete:
            await msg.reply_to_message.delete()

    if poll.is_closed:
        await msg.delete()
