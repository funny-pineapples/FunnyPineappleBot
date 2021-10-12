from datetime import datetime, timedelta

import mc
from shared.instances import dp, bot
from aiogram import types as t
from utils import filters as f
from shared import instances as ins

pin_reply_markup = t.InlineKeyboardMarkup().add(
    t.InlineKeyboardButton("Проверить сейчас", callback_data="chek")
)


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


@dp.message_handler(commands=["chance"])
async def закрепить_хуту(msg: t.Message):
    if msg.get_args():
        try:
            chance = int(msg.get_args().split()[0])
            if 0 <= chance <= 100:
                ins.gen_chance = chance
            else:
                raise RuntimeError()

            await msg.answer(f"Теперь я сру с шансом в: {chance}%")
        except Exception:
            await msg.answer("Я хз что не так, но я знаю что ты дебил \n    /chance <ЧИСЛО ОТ 0 ДО 100>")
    else:
        await msg.answer(f"Я сру с шансом в: {ins.gen_chance}%")


@dp.message_handler(f.message.chance, f.message.is_chat, content_types=[t.ContentType.ANY])
async def срать_сообщение_с_шансом(msg: t.Message):
    await сгенерировать_хуету(msg)


@dp.callback_query_handler(f.message.is_chat, lambda clb: clb.data == "chek")
async def проверить_опрос(clb: t.CallbackQuery):
    poll = clb.message.poll
    msg = clb.message

    if poll.total_voter_count <= 0:
        await clb.answer("Видишь голоса? Вот и я невижу")
    else:
        if not poll.is_closed:
            await bot.stop_poll(msg.chat.id, msg.message_id)
        await msg.delete_reply_markup()

        yes = poll.options[0].voter_count
        delete = poll.options[1].voter_count
        win = max(yes, delete)

        if win == yes:
            await msg.pin()
        elif win == delete:
            await msg.delete()
