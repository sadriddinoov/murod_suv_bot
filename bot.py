import os
import asyncio
from dotenv import load_dotenv

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django

django.setup()

from aiogram import Bot, Dispatcher
from tg_bot.handlers.start import router, set_bot_commands

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')


async def main():
    if not BOT_TOKEN:
        raise ValueError('BOT_TOKEN not found in .env')

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)

    await set_bot_commands(bot)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
