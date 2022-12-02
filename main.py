import logging

from aiogram import Dispatcher, executor
from aiogram import types as t

logging.basicConfig(level=logging.INFO)


async def on_start(dp: Dispatcher) -> None:
    from shared.commands import commands

    for scope, cmd in commands.items():
        await dp.bot.delete_my_commands(scope)
        await dp.bot.set_my_commands(cmd, scope)


if __name__ == "__main__":
    import handlers
    from shared.instances import dp

    dp.middleware.setup(handlers.middleware.MessageMiddleware())
    executor.start_polling(
        dp,
        allowed_updates=t.AllowedUpdates.all(),
        on_startup=on_start,
        skip_updates=True,
    )
