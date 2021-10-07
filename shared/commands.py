from aiogram.types import BotCommand as cmd, BotCommandScopeAllGroupChats as group

commands = {
    group(): [
        cmd('gen', 'Высрвть текст'),
        cmd('del', 'Смыть говно'),
        cmd('pin', 'Повесить говно на стенку'),
    ]
}
