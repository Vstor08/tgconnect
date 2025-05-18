from aiogram import Router, types, F
from config import ADMIN_ID
from utils import filters,paste_buffer
import logging
router = Router()

@router.message(filters.IsAdmin(ADMIN_ID),filters.Command("buffer"))
async def buffer(message: types.Message):
    args = message.text.split()[1:]
    try:
        paste_buffer.copy_to_clipboard(args[0])
        await message.answer("успешно добавлено в буфер обмена")
        logging.info(f"в буфер обмена добавлено {args[0]}")
    except:
        await message.answer("ошибка добавления в буфер обмена")
        logging.error("ошибка добавления в буфер обмена")
