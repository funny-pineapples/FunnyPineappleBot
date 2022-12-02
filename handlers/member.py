from aiogram import types as t

from shared.instances import bot, config, dp
from utils import filters as f


@dp.chat_join_request_handler()
async def new_member(cjr: t.ChatJoinRequest) -> None:
    reply = await bot.send_message(
        cjr.chat.id,
        f'<a href="tg://user?id={cjr.from_user.id}">{cjr.from_user.mention}</a> хочет в чат',
        parse_mode=t.ParseMode.HTML,
    )
    await reply.reply_poll(
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
async def check_poll(clb: t.CallbackQuery) -> None:
    poll = clb.message.poll
    msg = clb.message
    data = clb.data.split(":")
    user_id = int(data[1])
    min_answers = config.get_config(msg.chat.id).commands.accept_member_answers_count

    if poll.total_voter_count < min_answers:
        await clb.answer(
            f"Нужно хотябы {min_answers} голоса, сейчас {poll.total_voter_count}"
        )
    else:
        if not poll.is_closed:
            await bot.stop_poll(msg.chat.id, msg.message_id)

        if poll.options[0].voter_count > poll.options[1].voter_count:
            await bot.approve_chat_join_request(msg.chat.id, user_id)
            await bot.send_message(
                user_id, "Ваша заявка на вступление принята, добро пожаловать в группу"
            )
        else:
            await bot.decline_chat_join_request(msg.chat.id, user_id)
            await bot.send_message(user_id, "Ваша заявка на вступление НЕ принята")
            if not msg.chat.has_protected_content:
                await msg.forward(user_id)
