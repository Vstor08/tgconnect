import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import BOT_TOKEN
#from handlers.start import router
from utils.logger import setup_logger
from utils.setup_handlers import setup_all_routers
from utils.commands_db import CommandsDB

setup_logger()

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    CommandsDB("./data/commands.db")
    #dp.include_router(router)
    setup_all_routers(dp)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
