import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.fsm.strategy import FSMStrategy
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv  # ⬅️ Import dotenv

# ✅ Load .env file
load_dotenv()
API_TOKEN = os.getenv("BOT_TOKEN")

# ✅ Inisialisasi Bot dan Dispatcher
bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# ✅ Handler /start
@dp.message(Command("start"))
async def start_handler(message: Message):
    await message.answer(
        "<b>👋 Selamat datang di EA ICT by Nobita</b>\n\n"
        "Bot ini akan membantu kamu:\n"
        "• 📘 Memasang EA di MT5\n"
        "• 🧠 Mengenal strategi ICT\n"
        "• 🔔 Menerima sinyal dan notifikasi\n\n"
        "Gunakan perintah /menu untuk mulai ▶️"
    )

# ✅ Jalankan bot
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
