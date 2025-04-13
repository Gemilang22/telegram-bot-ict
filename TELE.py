import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.filters import Command

# Ganti ini dengan token bot Telegram kamu
API_TOKEN = '7830689776:AAFJabHa7QdnuKfz0b97N8x5TGsl9RPPBX0'

# Inisialisasi bot dan dispatcher
bot = Bot(token=API_TOKEN, default=types.DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# /start handler
@dp.message(Command("start"))
async def start_handler(message: Message):
    await message.answer(
        "<b>👋 Selamat datang di Bot EA ICT by Nobita!</b>\n\n"
        "Gunakan perintah /help untuk melihat panduan pemasangan EA ke MetaTrader 5.\n\n"
        "🚀 Siap trading otomatis dengan strategi ICT!"
    )

# /help handler - Panduan Pemasangan EA
@dp.message(Command("help"))
async def help_handler(message: Message):
    help_text = (
        "<b>📘 Panduan Pemasangan EA Bot di MetaTrader 5 (PC)</b>\n\n"
        "<b>1️⃣ Siapkan File EA (.ex5)</b>\n"
        "• Pastikan kamu sudah punya file EA, misalnya <i>ICT_Scalping.ex5</i>\n"
        "• Jika belum punya, silakan hubungi admin bot ini.\n\n"
        "<b>2️⃣ Buka MetaTrader 5</b>\n"
        "• Klik menu <b>File ➤ Open Data Folder</b>\n"
        "• Masuk ke folder <b>MQL5 ➤ Experts</b>\n"
        "• Copy dan paste file EA (.ex5) ke folder tersebut.\n\n"
        "<b>3️⃣ Restart MetaTrader 5</b>\n"
        "• Tutup dan buka kembali MetaTrader 5\n"
        "• EA akan muncul di bagian <b>Navigator ➤ Expert Advisors</b>\n\n"
        "<b>4️⃣ Pasang EA di Chart</b>\n"
        "• Buka chart pair (misalnya EURUSD, XAUUSD, atau BTCUSD)\n"
        "• Seret EA ke chart ➤ Centang <i>Allow Algo Trading</i>\n\n"
        "<b>5️⃣ Aktifkan AutoTrading</b>\n"
        "• Klik tombol <b>Algo Trading</b> di toolbar (warna hijau = aktif)\n\n"
        "<b>6️⃣ Selesai!</b>\n"
        "• EA kamu siap bekerja otomatis sesuai strategi ICT.\n\n"
        "<i>Pastikan koneksi internet stabil dan akun login di MetaTrader 5 aktif.</i>\n\n"
        "📬 Butuh bantuan lebih lanjut? Hubungi admin bot ini."
    )
    await message.answer(help_text)

# Fungsi utama untuk menjalankan bot
async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
