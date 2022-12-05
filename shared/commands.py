from aiogram.types import BotCommand as cmd
from aiogram.types import BotCommandScopeAllChatAdministrators as admin
from aiogram.types import BotCommandScopeAllGroupChats as group
from aiogram.types import BotCommandScopeAllPrivateChats as private

commands = {
    group(): [
        cmd("gen", "Сгенерировать сообщение"),
        cmd("pin", "Создать опрос для закрепления сообщения"),
    ],
    admin(): [
        cmd("gen", "Сгенерировать сообщение"),
        cmd("pin", "Создать опрос для закрепления сообщения"),
        cmd("void", "Отчистить связи для генерации сообщений"),
        cmd("config", "Открыть настройки чата"),
    ],
    private(): [
        cmd("gen", "Сгенерировать сообщение"),
        cmd("void", "Отчистить связи для генерации сообщений"),
    ],
}
