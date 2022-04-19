import logging
import traceback

from aiogram import types as t

from shared.instances import dp


@dp.errors_handler()
async def уборщик_какашек(upd: t.Update, err: Exception):
    txt = "Я хз что произошло, но да \n"
    txt += f"   {err.__class__.__name__}: {' '.join(map(str, err.args))}"

    if upd.message:
        await upd.message.answer(txt)
    elif upd.callback_query:
        await upd.callback_query.answer(txt)
    else:
        return

    logging.error(traceback.format_exc())

    return True
