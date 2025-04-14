import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.types import (
    Message, 
    InlineKeyboardMarkup, 
    InlineKeyboardButton, 
    CallbackQuery, 
    FSInputFile
)
from aiogram.filters import Command
from aiogram.client.default import DefaultBotProperties

# 🔐 TOKEN BOT
API_TOKEN = "7830689776:AAFJabHa7QdnuKfz0b97N8x5TGsl9RPPBX0"

# 🤖 Setup Bot & Dispatcher
bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# 📌 Inline Menu
def main_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📘 Panduan Pasang EA", callback_data="install_guide")],
        [InlineKeyboardButton(text="🧠 Tentang Strategi ICT", callback_data="ict_strategy")],
        [InlineKeyboardButton(text="📦 Download EA", callback_data="download_ea")],
        [InlineKeyboardButton(text="📞 Kontak Admin", url="https://t.me/NOBITA_291200")]
    ])

def back_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Kembali ke Menu", callback_data="back_to_menu")]
    ])

# 🚀 START
@dp.message(Command("start"))
async def start_handler(message: Message):
    await message.answer(
        "<b>👋 Selamat datang di EA ICT by Nobita</b>\n\n"
        "Bot ini akan membantu kamu:\n"
        "• 📘 Memasang EA di MT5\n"
        "• 🧠 Mengenal strategi ICT\n"
        "• 🔔 Menerima sinyal dan notifikasi\n\n"
        "Gunakan perintah /menu untuk mulai 🚀",
        reply_markup=main_menu()
    )

# ℹ️ HELP
@dp.message(Command("help"))
async def help_handler(message: Message):
    await message.answer(
        "<b>🛠 Panduan Pemasangan EA ICT by Nobita di MetaTrader 5 (PC)</b>\n\n"
        "1️⃣ File > Open Data Folder\n"
        "2️⃣ MQL5 > Experts > Tempel file EA (.ex5)\n"
        "3️⃣ Restart MT5 dan drag EA ke chart\n"
        "4️⃣ Aktifkan Auto Trading & Allow DLL\n\n"
        "Saran: Gunakan VPS untuk 24/7 trading! 🚀"
    )

# 📋 MENU
@dp.message(Command("menu"))
async def menu_handler(message: Message):
    await message.answer("<b>📋 MENU UTAMA</b>\nSilakan pilih menu di bawah ini 👇", reply_markup=main_menu())

# ⬅️ Kembali ke Menu
@dp.callback_query(lambda c: c.data == "back_to_menu")
async def back_to_menu(callback: CallbackQuery):
    await callback.message.edit_text("<b>📋 MENU UTAMA</b>\nSilakan pilih menu di bawah ini 👇", reply_markup=main_menu())
    await callback.answer()

# 📘 Panduan Install
@dp.callback_query(lambda c: c.data == "install_guide")
async def install_guide(callback: CallbackQuery):
    await callback.message.edit_text(
        "<b>📘 Cara Install EA di MetaTrader 5 (PC)</b>\n\n"
        "📁 File > Open Data Folder\n"
        "➡️ MQL5 > Experts\n"
        "📌 Paste file EA di folder tersebut\n"
        "🔄 Restart MT5 dan buka Navigator\n"
        "📊 Tarik EA ke chart dan centang Allow DLL & Auto Trading\n\n"
        "🟢 Siap! Gunakan VPS agar trading 24 jam nonstop.",
        reply_markup=back_menu()
    )
    await callback.answer()

# 🧠 Tentang Strategi ICT
@dp.callback_query(lambda c: c.data == "ict_strategy")
async def ict_strategy(callback: CallbackQuery):
    await callback.message.edit_text(
        "<b>🧠 Apa Itu Strategi ICT?</b>\n\n"
        "ICT (Inner Circle Trader) adalah strategi Smart Money Concept berbasis:\n"
        "✔️ Break of Structure (BOS)\n"
        "✔️ Order Block (OB)\n"
        "✔️ Fair Value Gap (FVG)\n\n"
        "EA kami fokus pada entry otomatis di TF kecil (M1–M15) menggunakan sinyal-sinyal ini.\n"
        "Cocok untuk scalping dengan winrate optimal! 🚀",
        reply_markup=back_menu()
    )
    await callback.answer()

# 📦 Kirim Link Download EA ICT By Nobita dari GitHub
@dp.callback_query(lambda c: c.data == "download_ea")
async def download_ea(callback: CallbackQuery):
    await callback.message.edit_text(
        "<b>📦 EA ICT Scalping by Nobita</b>\n\n"
        "🧠 Strategi: BOS, OB, FVG\n"
        "🕒 Timeframe: M1–M15 (Scalping)\n"
        "💾 Siap digunakan di MetaTrader 5\n\n"
        "⬇️ Klik link di bawah ini untuk mengunduh file EA:\n"
        "<a href='https://github.com/Gemilang22/telegram-bot-ict/blob/37c8b4956e0b421c399c7fc0ee7e55783b96c2dc/EA_ICT_SNR_By%20Nobita_v2.mq5'>📥 Download EA</a>\n\n"
        "📘 Ketik /help untuk panduan instalasi.",
        reply_markup=back_menu(),
        parse_mode=ParseMode.HTML
    )
    await callback.answer()


# 🔄 Jalankan Bot EA ICT by Nobita
async def main():
    print("🤖 Bot aktif dan siap melayani...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())