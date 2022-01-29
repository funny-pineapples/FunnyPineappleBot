import optparse

from aiogram import executor, types as t, Dispatcher
import logging

logging.basicConfig(level=logging.INFO)

async def on_start(dp: Dispatcher):
    from shared.commands import commands
    for scope, cmd in commands.items():
        await dp.bot.delete_my_commands(scope)
        await dp.bot.set_my_commands(cmd, scope)


if __name__ == '__main__':
    from shared.instances import dp
    import handlers

    executor.start_polling(
        dp, allowed_updates=t.AllowedUpdates.all(), on_startup=on_start, skip_updates=True
    )
