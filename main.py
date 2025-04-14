# main.py

import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
from handlers import register_handlers

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")  # Token diatur di file .env

# Setup Bot & Dispatcher
bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())

# Register semua handler
register_handlers(dp)

# Jalankan Bot
async def main():
    print("🤖 Bot aktif...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
