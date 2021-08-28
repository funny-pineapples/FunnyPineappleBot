import optparse

from aiogram import executor, types as t, Dispatcher
from shared.instances import dp, bot
import logging
from shared import config

logging.basicConfig(level=logging.INFO)

parser = optparse.OptionParser(conflict_handler="resolve")
parser.add_option('-t', '--test',
                  action="store_true",
                  dest='test',
                  help='test token')
parser.add_option('-m', '--main',
                  action="store_true",
                  dest='main',
                  help='main token')
values, args = parser.parse_args()

if values.test:
    config.token = config.test_token
elif values.main:
    config.token = config.main_token
else:
    config.token = config.test_token


async def on_start(dp: Dispatcher):
    from shared.commands import commands
    for scope, cmd in commands.items():
        await bot.set_my_commands(cmd, scope)


if __name__ == '__main__':
    import handlers

    executor.start_polling(
        dp, allowed_updates=t.AllowedUpdates.all(), on_startup=on_start
    )
