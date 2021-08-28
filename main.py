from aiogram import executor, types as t, Dispatcher
from shared.instances import dp, bot
import logging

logging.basicConfig(level=logging.INFO)


async def on_start(dp: Dispatcher):
    from shared.commands import commands
    for scope, cmd in commands.items():
        await bot.set_my_commands(cmd, scope)

if __name__ == '__main__':
    import handlers
    executor.start_polling(
        dp, allowed_updates=t.AllowedUpdates.all(), on_startup=on_start
    )
