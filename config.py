import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))
FSUB_CHANNEL_ID = int(os.getenv("FSUB_CHANNEL_ID", "-1002164685014"))
FSUB_CHANNEL_LINK = os.getenv("FSUB_CHANNEL_LINK", "https://t.me/MrBossTG")
DB_PATH = os.getenv("DB_PATH", "bot_database.db")
REPO_URL = os.getenv("REPO_URL", "https://github.com/MrBoss002/RichMDHelpBot")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is missing! Please add it in Render's Environment Variables.")
