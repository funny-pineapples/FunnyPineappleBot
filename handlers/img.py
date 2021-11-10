from os import system as run

from aiogram import types as t
from aiogram.dispatcher import filters

from handlers.gen import получить_говно
from shared.instances import dp, bot


async def скачать(name: str) -> str:
    msg = t.Message.get_current()
    if msg.content_type == t.ContentType.TEXT:
        if msg.reply_to_message is None:
            await msg.answer("Эээм… а где ответ ?")
            return
        msg = msg.reply_to_message

    if msg.content_type == t.ContentType.PHOTO:
        file_id = msg.photo[-1].file_id
    elif msg.content_type == t.ContentType.DOCUMENT:
        file_id = msg.document.file_id
    else:
        await msg.answer("Эээм… а где фото ?")
        return

    name = f"{name}.{msg.from_user.id}.{msg.chat.id}"
    await bot.download_file_by_id(file_id, destination=f"tmp/{name}.jpg")
    return name


def удалить(name: str):
    run(f"rm -rf tmp/*{name}*")


@dp.message_handler(
    filters.Command("gif", ignore_caption=False),
    content_types=[t.ContentType.PHOTO, t.ContentType.DOCUMENT, t.ContentType.TEXT],
)
async def высрать_гифку_по_фото(msg: t.Message):
    name = await скачать("gif")
    run(
        " ".join(
            [
                "ffmpeg -loglevel quiet -y",
                f"-i tmp/{name}.jpg",
                '-vf scale="ceil(iw/2)*2:ceil(ih/2)*2"',
                f"tmp/{name}.mp4",
            ]
        )
    )
    await msg.answer_animation(open(f"tmp/{name}.mp4", "rb"), caption=получить_говно())
    удалить(name)
