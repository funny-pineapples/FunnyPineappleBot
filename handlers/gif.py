from os import system as run

from aiogram import types as t
from aiogram.dispatcher import filters

from handlers.gen import получить_говно
from shared.instances import dp


@dp.message_handler(
    filters.Command("gif", ignore_caption=False),
    content_types=[t.ContentType.PHOTO, t.ContentType.DOCUMENT],
)
async def высрать_гифку_по_фото(msg: t.Message):
    await скачать_и_обработать_файл(msg)
    with open("tmp/gif.mp4", "rb") as file:
        await msg.reply_animation(file, caption=получить_говно())


@dp.message_handler(
    commands=["gif"],
    content_types=[t.ContentType.TEXT],
)
async def высрать_гифку_по_ответу(msg: t.Message):
    await скачать_и_обработать_файл(msg)
    with open("tmp/gif.mp4", "rb") as file:
        await msg.reply_animation(file, caption=получить_говно())


async def скачать_и_обработать_файл(msg: t.Message):
    tmp = "tmp/"
    inp = tmp + "gif.jpg"
    out = tmp + "gif.mp4"

    try:
        if msg.text:
            photo = msg.reply_to_message.photo
            document = msg.reply_to_message.document
        else:
            photo = msg.photo
            document = msg.document

        if photo:
            await photo[-1].download(destination_file=inp)
        elif document:
            await document.download(destination_file=inp)
        else:
            raise RuntimeError()
    except Exception:
        await msg.reply("Чел, ответь на фото или пришли мне его")
        return

    run(f"ffmpeg -y -i {inp} {out}")
