import os
import asyncio
from dotenv import load_dotenv

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django
django.setup()

from aiogram import Bot, Dispatcher
from tg_bot.handlers.start import router as start_router, set_bot_commands
from tg_bot.handlers.products import router as products_router
from tg_bot.handlers.settings import router as settings_router
from tg_bot.handlers.feedback import router as feedback_router
from tg_bot.handlers.help import router as help_router

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")


async def main():
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN not found in .env")

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(start_router)
    dp.include_router(settings_router)
    dp.include_router(feedback_router)
    dp.include_router(help_router)
    dp.include_router(products_router)

    await set_bot_commands(bot)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())