from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
import logging
from config import ADMIN_ID
from utils import filters
from utils.commands_db import CommandsDB

router = Router()
db = CommandsDB("./data/commands.db")

# Состояния для FSM
class AddCommand(StatesGroup):
    waiting_for_name = State()
    waiting_for_command = State()

# Сборка клавиатуры
def build_commands_keyboard():
    commands = db.list_commands()
    buttons = [
         [InlineKeyboardButton(text="🔴 Удалить команду", callback_data="delete_command")]
        ,[InlineKeyboardButton(text="➕ Добавить команду", callback_data="add_command")]]
    for name in commands.keys():
        buttons.append([InlineKeyboardButton(text=name, callback_data=f"exec:{name}")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

# Хендлер "команды"
@router.message(filters.IsAdmin(ADMIN_ID), F.text.lower() == "команды")
async def command_list(message: types.Message):
    logging.info("обработка сообщения команды")
    keyboard = build_commands_keyboard()
    await message.answer("Выберите команду или добавьте новую:", reply_markup=keyboard)

# Хендлер кнопки выполнения команды
@router.callback_query(F.data.startswith("exec:"))
async def execute_command(callback: CallbackQuery):
    name = callback.data.split(":", 1)[1]
    command = db.get_command(name)

    if not command:
        await callback.answer("Команда не найдена", show_alert=True)
        return

    import subprocess
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=10)
        output = result.stdout.strip() or result.stderr.strip() or "Команда выполнена."
    except Exception as e:
        output = f"Ошибка выполнения: {e}"

    await callback.answer("Команда выполнена.", show_alert=False)
    await callback.message.answer(f"📦 <b>{name}</b>\n<pre>{output}</pre>", parse_mode="HTML")

# Хендлер кнопки "добавить команду"
@router.callback_query(F.data == "add_command")
async def ask_command_name(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AddCommand.waiting_for_name)
    await callback.message.answer("Введите <b>имя новой команды</b>:", parse_mode="HTML")
    await callback.answer()

# Получаем имя команды
@router.message(AddCommand.waiting_for_name)
async def receive_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text.strip())
    await state.set_state(AddCommand.waiting_for_command)
    await message.answer("Теперь введите <b>текст команды</b>:", parse_mode="HTML")

# Получаем команду и сохраняем
@router.message(AddCommand.waiting_for_command)
async def receive_command(message: types.Message, state: FSMContext):
    data = await state.get_data()
    name = data["name"]
    command = message.text.strip()

    if db.add_command(name, command):
        await message.answer(f"✅ Команда <b>{name}</b> добавлена.", parse_mode="HTML")
    else:
        await message.answer("⚠️ Не удалось добавить команду.", parse_mode="HTML")

    await state.clear()


class DeleteCommand(StatesGroup):
    waiting_for_name = State()

@router.callback_query(F.data == "delete_command")
async def ask_delete_name(callback: CallbackQuery, state: FSMContext):
    await state.set_state(DeleteCommand.waiting_for_name)
    await callback.message.answer("Введите имя команды, которую нужно удалить:")
    await callback.answer()

@router.message(DeleteCommand.waiting_for_name)
async def receive_delete_name(message: types.Message, state: FSMContext):
    name = message.text.strip()

    if db.delete_command(name):
        await message.answer(f"✅ Команда <b>{name}</b> успешно удалена.", parse_mode="HTML")
    else:
        await message.answer(f"⚠️ Команда <b>{name}</b> не найдена.", parse_mode="HTML")

    await state.clear()
