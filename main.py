import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from handlers import register_handlers

# GANTI DENGAN TOKEN BOT KAMU LANGSUNG DI SINI
API_TOKEN = "7830689776:AAFJabHa7QdnuKfz0b97N8x5TGsl9RPPBX0"  # contoh

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
