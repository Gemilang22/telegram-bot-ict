import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import Command
from aiogram.client.default import DefaultBotProperties

# 🔐 Langsung masukkan token di sini
API_TOKEN = "7830689776:AAFJabHa7QdnuKfz0b97N8x5TGsl9RPPBX0"

# 🧠 Setup Bot dan Dispatcher
bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# ✅ Command /start
@dp.message(Command("start"))
async def start_handler(message: Message):
    await message.answer(
        "<b>👋 Selamat datang di EA ICT by Nobita</b>\n\n"
        "Bot ini akan membantu kamu:\n"
        "• 📘 Memasang EA di MT5\n"
        "• 🧠 Mengenal strategi ICT\n"
        "• 🔔 Menerima sinyal dan notifikasi\n\n"
        "Gunakan perintah /menu untuk mulai ▶️",
    )

# ✅ Command /help
@dp.message(Command("help"))
async def help_handler(message: Message):
    await message.answer(
        "<b>🛠 Panduan Pemasangan EA MetaTrader 5 (PC)</b>\n\n"
        "1️⃣ Buka MetaTrader 5 > File > Open Data Folder\n"
        "2️⃣ Masuk ke folder <b>MQL5 > Experts</b>\n"
        "3️⃣ Tempel file EA (.ex5) ke folder tersebut\n"
        "4️⃣ Tutup dan buka kembali MetaTrader 5\n"
        "5️⃣ Di Navigator, tarik EA ke dalam chart\n"
        "6️⃣ Centang opsi 'Allow DLL imports' & 'Algo Trading'\n\n"
        "⚙️ EA akan mulai berjalan secara otomatis!\n"
        "Disarankan menggunakan VPS agar tetap online 24 jam nonstop 🚀"
    )

# ✅ Command /menu
@dp.message(Command("menu"))
async def menu_handler(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📘 Panduan Pasang EA", callback_data="install_guide")],
        [InlineKeyboardButton(text="🧠 Tentang Strategi ICT", callback_data="ict_strategy")],
        [InlineKeyboardButton(text="📞 Kontak Admin", url="https://t.me/nobita_fx")]
    ])

    await message.answer(
        "<b>📋 MENU UTAMA</b>\n\n"
        "Silakan pilih salah satu menu berikut untuk informasi lengkap 👇",
        reply_markup=keyboard
    )

# ✅ Callback: Panduan Install EA
@dp.callback_query(lambda c: c.data == "install_guide")
async def install_guide_callback(callback: CallbackQuery):
    await callback.message.edit_text(
        "<b>📘 Cara Install EA MetaTrader 5 (PC)</b>\n\n"
        "✅ Buka MT5 > File > Open Data Folder\n"
        "✅ Buka folder MQL5 > Experts\n"
        "✅ Tempel file EA (.ex5)\n"
        "✅ Restart MT5, buka chart, drag EA ke chart\n"
        "✅ Aktifkan Auto Trading dan centang Allow DLL\n\n"
        "🟢 EA Siap digunakan! Gunakan VPS agar tetap aktif 24 jam!"
    )
    await callback.answer()

# ✅ Callback: Tentang ICT
@dp.callback_query(lambda c: c.data == "ict_strategy")
async def ict_strategy_callback(callback: CallbackQuery):
    await callback.message.edit_text(
        "<b>🧠 Apa Itu Strategi ICT?</b>\n\n"
        "Strategi ICT (Inner Circle Trader) adalah pendekatan price action profesional berbasis:\n"
        "• Break of Structure (BOS)\n"
        "• Order Block (OB)\n"
        "• Fair Value Gap (FVG)\n"
        "• Smart Money Concept (SMC)\n\n"
        "EA kami dirancang untuk entry otomatis berbasis BOS & FVG pada TF kecil (M1–M15) ✨"
    )
    await callback.answer()

# ✅ Main Entry Point
async def main():
    print("🤖 Bot sedang berjalan...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
