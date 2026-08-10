import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

import config
from database import init_db
from middlewares.fsub import ForceSubMiddleware

# Enable logging
logging.basicConfig(level=logging.INFO)

async def main():
    # Initialize SQLite tables on startup
    await init_db()

    bot = Bot(
        token=config.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()

    # Register Forced Subscription Middleware across all outer message handlers
    dp.message.outer_middleware(ForceSubMiddleware())
    dp.callback_query.outer_middleware(ForceSubMiddleware())

    logging.info("Starting RichMDHelpBot with FSub enabled...")
    
    # Handlers will be registered here in Phase 3
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
