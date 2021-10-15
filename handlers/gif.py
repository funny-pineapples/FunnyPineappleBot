from os import system as run

from aiogram import types as t
from aiogram.dispatcher import filters

from handlers.gen import получить_говно
from shared.instances import dp


@dp.message_handler(
    filters.Command("gif", ignore_caption=False),
    content_types=[t.ContentType.PHOTO, t.ContentType.DOCUMENT, t.ContentType.TEXT],
    commands=["gif"]
)
async def высрать_гиф(msg: t.Message):
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

    run(f"ffmpeg -loglevel quiet -y -i {inp} {out}")

    with open(out, "rb") as file:
        await msg.reply_animation(file, caption=получить_говно())
