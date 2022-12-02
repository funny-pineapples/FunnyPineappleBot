import logging
import traceback

from aiogram import types as t

from shared.instances import dp


@dp.errors_handler()
async def error_handler(upd: t.Update, err: Exception) -> bool:
    if isinstance(err, AssertionError):
        text = " ".join(map(str, err.args))
    else:
        text = f"{err.__class__.__name__}: {' '.join(map(str, err.args))}"

    if upd.message:
        await upd.message.answer(text)
    elif upd.callback_query:
        await upd.callback_query.answer(text)
    else:
        return False

    if not isinstance(err, AssertionError):
        logging.error(traceback.format_exc())

    return True
