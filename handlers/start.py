from aiogram import Router, types, F
from config import ADMIN_ID
from utils import keyboards, filters,os_info
import logging
router = Router()

@router.message(filters.IsAdmin(ADMIN_ID),filters.Command("start"))
async def start_cmd(message: types.Message):
    await message.answer(f"TGConnect запущен и работает\nЗапущено на: {os_info.parse_os_release()["NAME"]}\nHOSTNAME: {os_info.parse_hostname()}",reply_markup=keyboards.main_menu)
    logging.info(f"start handler called, user: {message.from_user.id}")
