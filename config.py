from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = str(os.getenv("BOT_TOKEN"))
ADMIN_ID = str(os.getenv("ADMIN_ID"))
