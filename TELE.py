import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

# Ganti dengan token bot kamu
API_TOKEN = "7830689776:AAFJabHa7QdnuKfz0b97N8x5TGsl9RPPBX0"

# Inisialisasi bot dan dispatcher
bot = Bot(
    token=API_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

# Handler saat user kirim pesan /start
@dp.message(F.text == "/start")
async def handle_start(message: Message):
    await message.answer(
        "👋 <b>Selamat datang di Bot ICT EA!</b>\n"
        "Bot ini siap membantu kamu menjalankan Expert Advisor dan memberikan notifikasi trading.\n\n"
        "📌 Ketik /help untuk melihat menu bantuan."
    )

# Handler untuk /help
@dp.message(F.text == "/help")
async def handle_help(message: Message):
    await message.answer(
        "🛠 <b>Menu Bantuan</b>\n\n"
        "✅ /start - Mulai bot\n"
        "✅ /help - Lihat bantuan\n"
        "📨 Kirim pesan apapun untuk respon otomatis"
    )

# Respon default untuk pesan lain
@dp.message()
async def handle_message(message: Message):
    await message.answer("📩 Pesan kamu telah diterima. Tim kami akan segera merespons!")

# Fungsi utama untuk menjalankan bot
async def main():
    print("🤖 Bot Telegram telah dijalankan...")
    await dp.start_polling(bot)

# Jalankan bot dengan asyncio
if __name__ == "__main__":
    asyncio.run(main())
