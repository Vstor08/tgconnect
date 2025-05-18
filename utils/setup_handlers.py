import os
import importlib
from aiogram import Dispatcher

def setup_all_routers(dp: Dispatcher, handlers_dir="handlers"):
    for filename in os.listdir(handlers_dir):
        if filename.endswith(".py") and not filename.startswith("__"):
            module_name = f"{handlers_dir}.{filename[:-3]}"
            module = importlib.import_module(module_name)
            router = getattr(module, "router", None)
            if router:
                dp.include_router(router)
