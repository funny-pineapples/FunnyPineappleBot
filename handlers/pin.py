from datetime import datetime, timedelta

from aiogram import types as t

from shared.instances import bot, dp
from utils import filters as f


@dp.message_handler(f.message.is_chat, commands=["pin"])
async def закрепить_хуету(msg: t.Message):
    await msg.delete()
    if msg.reply_to_message:
        r = await msg.reply_to_message.reply(
            f'<a href="tg://user?id={msg.from_user.id}">{msg.from_user.mention}</a> хочет закрепить сообщение',
            parse_mode=t.ParseMode.HTML,
        )
        await r.reply_poll(
            "Закрепить ?",
            ["Да", "УДАЛИ НАХУЙ", "Нет"],
            close_date=datetime.now() + timedelta(minutes=10),
            reply_markup=t.InlineKeyboardMarkup().add(
                t.InlineKeyboardButton(
                    "Проверить опрос",
                    callback_data=f"check_pin_poll:{msg.reply_to_message.id}",
                )
            ),
        )
    else:
        await msg.answer("Ты умник, ответь на сообщение")


@dp.callback_query_handler(
    f.message.is_chat, lambda clb: clb.data.split(":")[0] == "check_pin_poll"
)
async def проверить_закреп(clb: t.CallbackQuery):
    poll = clb.message.poll
    msg = clb.message
    pin = int(clb.data.split(":")[1])

    if poll.total_voter_count < 2:
        await clb.answer(f"Нужно хотябы 2 голоса, сейчас {poll.total_voter_count}")
    else:
        if not poll.is_closed:
            await bot.stop_poll(msg.chat.id, msg.message_id)

        yes = poll.options[0].voter_count
        delete = poll.options[1].voter_count
        win = max(yes, delete)

        if win == yes:
            await msg.chat.pin_message(pin)
        elif win == delete:
            await msg.chat.delete_message(pin)
        await msg.delete()
