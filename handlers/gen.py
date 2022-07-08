import mc
from aiogram import types as t

from shared import instances as ins
from shared.instances import bot, dp
from utils import filters as f


@dp.message_handler(commands=["gen"])
async def сгенерировать_хуету(msg: t.Message):
    await msg.answer(получить_говно(msg.chat.id))


@dp.message_handler(commands=["del"])
async def удалить_хуету(msg: t.Message):
    await msg.delete()

    if msg.reply_to_message:
        if msg.reply_to_message.from_user.id in [bot.id, msg.from_user.id]:
            await msg.reply_to_message.delete()
        else:
            await msg.answer("Ты умник, можно только свои или мои удалять")
    else:
        await msg.answer("Ты умник, ответь на сообщение")


@dp.message_handler(commands=["chance"])
async def изменить_шанс_срания(msg: t.Message):
    if msg.get_args():
        try:
            chance = int(msg.get_args().split()[0])
            if 0 <= chance <= 100:
                ins.gen_chance[msg.chat.id] = chance
            else:
                raise RuntimeError()

            await msg.answer(f"Теперь я сру с шансом в: {chance}%")
        except Exception:
            await msg.answer(
                "Я хз что не так, но я знаю что ты дебил \n    /chance <ЧИСЛО ОТ 0 ДО 100>"
            )
    else:
        await msg.answer(f"Я сру с шансом в: {ins.gen_chance.get(msg.chat.id, 10)}%")


@dp.message_handler(f.message.chance, content_types=[t.ContentType.ANY])
async def срать_сообщение_с_шансом(msg: t.Message):
    await msg.answer(получить_говно(msg.chat.id))


def получить_говно(id: int) -> str:
    samples = mc.util.load_txt_samples(f"data/{id}", separator="§")
    return mc.StringGenerator(samples=samples).generate_string()
