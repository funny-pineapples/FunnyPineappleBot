from aiogram import types as t

from shared.instances import bot, dp
from utils import filters as f


@dp.chat_join_request_handler()
async def приём_запроса(cjr: t.ChatJoinRequest):
    r = await bot.send_message(
        cjr.chat.id,
        f'<a href="tg://user?id={cjr.from_user.id}">{cjr.from_user.mention}</a> хочет в чат',
        parse_mode=t.ParseMode.HTML,
    )
    await r.reply_poll(
        "Пускаем ?",
        [
            "Да",
            "Нет",
        ],
        False,
        reply_markup=t.InlineKeyboardMarkup().add(
            t.InlineKeyboardButton(
                "Проверить опрос",
                callback_data=f"check_request_poll:{cjr.from_user.id}",
            )
        ),
    )
    await bot.send_message(
        cjr.from_user.id, "Заявка на вступление в группу будет вскоре рассмотрена"
    )


@dp.callback_query_handler(
    f.message.is_chat, lambda clb: clb.data.split(":")[0] == "check_request_poll"
)
async def проверить_запрос(clb: t.CallbackQuery):
    poll = clb.message.poll
    msg = clb.message
    data = clb.data.split(":")
    user_id = int(data[1])

    if poll.total_voter_count < 4:
        await clb.answer(f"Нужно хотябы 4 голоса, сейчас {poll.total_voter_count}")
    else:
        if not poll.is_closed:
            await bot.stop_poll(msg.chat.id, msg.message_id)

        yes = poll.options[0].voter_count
        no = poll.options[1].voter_count
        win = max(yes, no)

        if win == yes:
            await bot.approve_chat_join_request(msg.chat.id, user_id)
            await bot.send_message(
                user_id, "Ваша заявка на вступление принята, добро пожаловать в группу"
            )
        elif win == no:
            await bot.decline_chat_join_request(msg.chat.id, user_id)
            await bot.send_message(user_id, "Ваша заявка на вступление НЕ принята")
            if not msg.chat.has_protected_content:
                await msg.forward(user_id)
