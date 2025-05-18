import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BufferedInputFile
from config import BOT_TOKEN, ADMIN_ID
from utils.logger import setup_logger
from utils.setup_handlers import setup_all_routers
from utils.commands_db import CommandsDB

from fastapi import FastAPI, Request, UploadFile, File
import uvicorn

# --- FastAPI setup ---
app = FastAPI()
notify_queue = asyncio.Queue()

@app.post("/notify")
async def notify(request: Request):
    data = await request.json()
    text = data.get("text")
    if text:
        await notify_queue.put(text)
        return {"status": "ok"}
    return {"status": "error", "message": "No text provided"}

@app.post("/send-file")
async def send_file(file: UploadFile = File(...)):
    # читаем содержимое
    contents = await file.read()
    await notify_queue.put(("file", file.filename, contents))
    return {"status": "ok"}


# --- Start everything ---
setup_logger()

async def notifier(bot: Bot, chat_id: int):
    await bot.send_message(chat_id,"TGConnect Запущен")
    while True:
        item = await notify_queue.get()

        if isinstance(item, str):
            await bot.send_message(chat_id, item)
        elif isinstance(item, tuple) and item[0] == "file":
                _, filename, content = item
                file = BufferedInputFile(content, filename=filename)
                await bot.send_document(chat_id, document=file)

async def start_bot_and_api():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    CommandsDB("./data/commands.db")
    setup_all_routers(dp)

    # Запускаем отправку уведомлений
    asyncio.create_task(notifier(bot, ADMIN_ID))

    # Запускаем FastAPI сервер
    config = uvicorn.Config(app, host="127.0.0.1", port=8899, log_level="info")
    server = uvicorn.Server(config)
    asyncio.create_task(server.serve())

    # Запускаем бота
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(start_bot_and_api())
