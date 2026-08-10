import aiosqlite
import config

async def init_db():
    async with aiosqlite.connect(config.DB_PATH) as db:
        # Table to store unique bot users for /stats and /broadcast
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        # Table to store channel footer preferences
        await db.execute("""
            CREATE TABLE IF NOT EXISTS channels (
                chat_id INTEGER PRIMARY KEY,
                footer_text TEXT DEFAULT ''
            )
        """)
        await db.commit()

async def add_user(user_id: int):
    async with aiosqlite.connect(config.DB_PATH) as db:
        await db.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
        await db.commit()

async def get_total_users() -> int:
    async with aiosqlite.connect(config.DB_PATH) as db:
        async with db.execute("SELECT COUNT(*) FROM users") as cursor:
            result = await cursor.fetchone()
            return result[0] if result else 0

async def get_all_users():
    async with aiosqlite.connect(config.DB_PATH) as db:
        async with db.execute("SELECT user_id FROM users") as cursor:
            rows = await cursor.fetchall()
            return [row[0] for row in rows]

# Channel Management 
      async def set_channel_footer(chat_id: int, footer_text: str):
    async with aiosqlite.connect(config.DB_PATH) as db:
        await db.execute("""
            INSERT INTO channels (chat_id, footer_text) VALUES (?, ?)
            ON CONFLICT(chat_id) DO UPDATE SET footer_text = excluded.footer_text
        """, (chat_id, footer_text))
        await db.commit()

async def get_channel_footer(chat_id: int) -> str:
    async with aiosqlite.connect(config.DB_PATH) as db:
        async with db.execute("SELECT footer_text FROM channels WHERE chat_id = ?", (chat_id,)) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else ""

async def delete_channel_footer(chat_id: int):
    async with aiosqlite.connect(config.DB_PATH) as db:
        await db.execute("DELETE FROM channels WHERE chat_id = ?", (chat_id,))
        await db.commit()
