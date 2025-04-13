import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.client.default import DefaultBotProperties

API_TOKEN = "7830689776:AAFJabHa7QdnuKfz0b97N8x5TGsl9RPPBX0"

# Inisialisasi bot
bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# Handler pesan
@dp.message()
async def handle_message(message: Message):
    response = (
        "<b>🧠 Bot ICT Scalping by Nobita</b>\n"
        "📈 <b>Smart Trading Assistant untuk MetaTrader 5</b>\n\n"
        "🚀 Siap bantu deteksi:\n"
        "▫️ <b>Break of Structure (BOS)</b>\n"
        "▫️ <b>Fair Value Gap (FVG)</b>\n"
        "▫️ <b>Order Block (OB)</b>\n"
        "▫️ Entry Signal otomatis\n\n"
        "📲 <i>Gunakan bersama EA MetaTrader 5 kamu!</i>\n"
        "💬 Ketik <b>/help</b> untuk info lebih lanjut."
    )
    await message.answer(response)

# Fungsi utama
async def main():
    await dp.start_polling(bot)

# Eksekusi program
if __name__ == "__main__":
    asyncio.run(main())
