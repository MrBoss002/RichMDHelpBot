import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

import config
from database import init_db
from middlewares.fsub import ForceSubMiddleware
from handlers import start, admin, formatter

# Enable logging
logging.basicConfig(level=logging.INFO)

async def main():
    # Initialize SQLite database schema
    await init_db()

    bot = Bot(
        token=config.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()

    # Register Forced Subscription Middleware
    dp.message.outer_middleware(ForceSubMiddleware())
    dp.callback_query.outer_middleware(ForceSubMiddleware())

    # Include Router Handlers
    dp.include_router(start.router)
    dp.include_router(admin.router)
    dp.include_router(formatter.router)

    logging.info("Starting RichMDHelpBot with FSub enabled...")
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
