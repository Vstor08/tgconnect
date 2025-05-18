import os
from aiogram import Router, types, F
from aiogram.types import Message
from pathlib import Path

router = Router()

DOWNLOAD_DIR = Path.home() / "Downloads" / "tgconn"
DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.message(F.document | F.photo | F.video | F.audio | F.voice)
async def save_file(message: Message, bot):
    file = None
    filename = "unknown"

    if message.document:
        file = message.document
        filename = file.file_name
    elif message.photo:
        file = message.photo[-1]  # highest resolution
        filename = f"photo_{file.file_id}.jpg"
    elif message.video:
        file = message.video
        filename = f"video_{file.file_id}.mp4"
    elif message.audio:
        file = message.audio
        filename = file.file_name or f"audio_{file.file_id}.mp3"
    elif message.voice:
        file = message.voice
        filename = f"voice_{file.file_id}.ogg"

    if file is None:
        await message.answer("Не удалось определить файл.")
        return

    path = DOWNLOAD_DIR / filename

    file_obj = await bot.get_file(file.file_id)
    await bot.download_file(file_obj.file_path, destination=path)

    await message.answer(f"📥 Файл сохранён как:\n<code>{path}</code>", parse_mode="HTML")
