import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))
FSUB_CHANNEL = os.getenv("FSUB_CHANNEL", "MrBossTG")
DB_PATH = os.getenv("DB_PATH", "bot_database.db")
REPO_URL = os.getenv("REPO_URL", "https://github.com/MrBoss002/RichMDHelpBot")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is missing in .env file!")
