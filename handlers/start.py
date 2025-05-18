from aiogram import Router, types, F
from config import ADMIN_ID

router = Router()

@router.message(F.from_user.id == ADMIN_ID, F.text == "/start")
async def start_cmd(message: types.Message):
    await message.answer("Привет! TgConnect готов к работе.")
