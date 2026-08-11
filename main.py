import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiohttp import web

import config
from database import init_db
from middlewares.fsub import ForceSubMiddleware
from handlers import start, admin, formatter

# Enable logging
logging.basicConfig(level=logging.INFO)

# Dummy web server endpoint to satisfy Render's Free Web Service port check
async def handle_ping(request):
    return web.Response(text="RichMDHelpBot is active!")

async def start_web_server():
    app = web.Application()
    app.router.add_get("/", handle_ping)
    
    # Read PORT provided by Render (defaults to 10000)
    port = int(os.getenv("PORT", 10000))
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    logging.info(f"Web server started on port {port} for Render health check.")

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

    # Start web server task concurrently in the background
    asyncio.create_task(start_web_server())

    logging.info("Starting RichMDHelpBot with FSub enabled...")
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
