from aiogram import types as t

from shared.instances import bot, chats, dp
from utils import filters as f


@dp.message_handler(f.message.is_chat, commands=["pin"])
async def pin_command(msg: t.Message) -> None:
    await msg.delete()
    if msg.reply_to_message:
        reply = await msg.reply_to_message.reply(
            f'<a href="tg://user?id={msg.from_user.id}">{msg.from_user.mention}</a> хочет закрепить сообщение',
            parse_mode=t.ParseMode.HTML,
        )
        await reply.reply_poll(
            "Закрепить сообщение ?",
            [
                "Да",
                "Нет",
            ],
            chats.get(msg.chat.id).pin.anonym,
            reply_markup=t.InlineKeyboardMarkup().add(
                t.InlineKeyboardButton(
                    "Проверить опрос",
                    callback_data=f"check_pin_poll:{msg.reply_to_message.message_id}",
                )
            ),
        )
    else:
        await msg.answer("Вы не ответили на сообщение")


@dp.callback_query_handler(
    f.message.is_chat, lambda clb: clb.data.split(":")[0] == "check_pin_poll"
)
async def check_poll(clb: t.CallbackQuery) -> None:
    poll = clb.message.poll
    msg = clb.message
    pin = int(clb.data.split(":")[1])
    min_answers = chats.get(msg.chat.id).pin.answer_count

    if poll.total_voter_count < min_answers:
        await clb.answer(
            f"Нужно хотябы {min_answers} голоса, сейчас {poll.total_voter_count}"
        )
    else:
        if poll.options[0].voter_count > poll.options[1].voter_count:
            await msg.chat.pin_message(pin)
        if not poll.is_closed:
            await bot.stop_poll(msg.chat.id, msg.message_id)
