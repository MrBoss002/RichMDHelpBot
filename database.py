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

      
