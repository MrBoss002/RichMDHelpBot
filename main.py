import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

import config

# Enable logging
logging.basicConfig(level=logging.INFO)

async def main():
    bot = Bot(
        token=config.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()

    logging.info("Starting RichMDHelpBot...")
    
    # We will register handlers and middlewares here in Phase 2 & 3
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
