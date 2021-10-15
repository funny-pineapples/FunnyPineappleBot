from aiogram.types import \
    BotCommand as cmd, \
    BotCommandScopeAllGroupChats as group, \
    BotCommandScopeAllPrivateChats as private

commands = {
    group(): [
        cmd('gen', 'Высрвть текст'),
        cmd('del', 'Смыть говно'),
        cmd('pin', 'Повесить говно на стенку'),
        cmd('gif', 'Превратить картинку в gif'),
        cmd('chance', 'Установить шанс высирания говна')
    ],
    private(): [
        cmd('gif', 'Превратить картинку в gif')
    ]
}
