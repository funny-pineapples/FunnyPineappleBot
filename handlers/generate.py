from datetime import datetime, timedelta

import mc
from shared.instances import dp, bot
from aiogram import types as t
from utils import filters as f

poll_ids = {}


@dp.message_handler(f.message.is_chat, commands=['gen'])
async def сгенерировать_хуету(msg: t.Message):
    samples = mc.util.load_txt_samples('samples.txt', separator='§')
    await msg.answer(mc.StringGenerator(samples=samples).generate_string())


@dp.message_handler(f.message.is_chat, commands=["del"])
async def удалить_хуету(msg: t.Message):
    await msg.delete()

    if msg.reply_to_message:
        if msg.reply_to_message.from_user.id in [bot.id, msg.from_user.id]:
            await msg.reply_to_message.delete()
        else:
            await msg.answer("Ты умник, можно только свои или мои удалять")
    else:
        await msg.answer("Ты умник, ответь на сообщение")


@dp.message_handler(f.message.is_chat, commands=["pin"])
async def закрепить_хуету(msg: t.Message):
    await msg.delete()

    btns = t.InlineKeyboardMarkup().add(
        t.InlineKeyboardButton("Проверить сейчас", callback_data="chek")
    )

    if msg.reply_to_message:
        if msg.reply_to_message.from_user.id == bot.id:
            poll = await msg.reply_to_message.reply_poll(
                "Закрепить ?",
                [
                    "Да",
                    "УДАЛИ НАХУЙ",
                    "Нет"
                ],
                close_date=datetime.now() + timedelta(minutes=10),
                reply_markup=btns
            )

            poll_ids[poll.poll.id] = msg.reply_to_message

        else:
            await msg.answer("Ты умник, можно только мои закреплять")
    else:
        await msg.answer("Ты умник, ответь на сообщение")


@dp.message_handler(f.message.chance(10), f.message.is_chat, content_types=[t.ContentType.ANY])
async def срать_сообщение_с_шансом(msg: t.Message):
    await сгенерировать_хуету(msg)


@dp.poll_handler()
async def время_вышло(poll: t.Poll):
    if poll.is_closed and poll.total_voter_count > 0:
        yes = poll.options[0].voter_count
        delete = poll.options[1].voter_count
        win = max(yes, delete)

        try:
            msg: t.Message = poll_ids.pop(poll.id)
        except KeyError:
            return

        if win == yes:
            await msg.pin()
        elif win == delete:
            await msg.delete()


@dp.callback_query_handler(f.message.is_chat, lambda clb: clb.data == "chek")
async def проверить_опрос(clb: t.CallbackQuery):
    await bot.stop_poll(clb.message.chat.id, clb.message.message_id)
