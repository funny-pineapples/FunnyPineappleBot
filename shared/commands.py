from aiogram.types import BotCommand as cmd
from aiogram.types import BotCommandScopeAllGroupChats as group
from aiogram.types import BotCommandScopeAllPrivateChats as private

commands = {
    group(): [
        cmd("gen", "Покакать текстом"),
        cmd("del", "Убрать говно"),
        cmd("void", "Лоботомия"),
        cmd("pin", "Закрепить говно"),
        cmd("chance", "Установить шанс покакать в туалет"),
    ],
    private(): [
        cmd("gen", "Покакать текстом"),
        cmd("del", "Убрать говно"),
        cmd("void", "Лоботомия"),
        cmd("chance", "Установить шанс покакать в туалет"),
    ],
}
