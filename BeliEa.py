import logging
import asyncio
import platform
from aiogram import Bot, Dispatcher, F, types
from aiogram.enums import ParseMode
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.client.default import DefaultBotProperties

API_TOKEN = '7830689776:AAFJabHa7QdnuKfz0b97N8x5TGsl9RPPBX0'
ADMIN_ID = 8081196747
CHANNEL_LINK = "https://t.me/+Y0uwuenHK9s3ZmQ1"

bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

class PurchaseForm(StatesGroup):
    uploading_proof = State()

# 🔘 MENU UTAMA
@dp.message(F.text.in_(['/start', '/menu']))
async def cmd_menu(message: types.Message):
    text = (
        "🎯 <b>Selamat datang di Bot Penjualan EA ICT Pro Scalper!</b>\n\n"
        "🧠 Strategi: ICT + Smart Money + Candlestick\n"
        "💹 Auto Risk 1%, Trailing Stop, Breakeven\n"
        "🕐 Multi Timeframe + GUI Kill Zone\n\n"
        "📌 Silakan pilih menu di bawah:"
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📘 Deskripsi EA", callback_data="desc")],
        [InlineKeyboardButton(text="💰 Beli Sekarang", callback_data="buy")],
        [InlineKeyboardButton(text="❓ Bantuan", callback_data="help")],
        [InlineKeyboardButton(text="💬 Chat Admin", url="https://t.me/NOBITA_291200")]
    ])
    await message.answer(text, reply_markup=keyboard)

# 🧾 DESKRIPSI EA
@dp.callback_query(F.data == "desc")
async def callback_desc(callback: types.CallbackQuery):
    text = (
        "📘 <b>ICT Pro Scalper v3.1</b>\n\n"
        "🚀 Fitur:\n"
        "• Entry BOS + OB + FVG + Candlestick\n"
        "• Multi Timeframe Filter (M15 & M5)\n"
        "• Kill Zone Asia, London, NY\n"
        "• Auto SL/TP, Breakeven, Trailing\n"
        "• Telegram Notifikasi\n"
        "• Max 1 Posisi Aktif\n\n"
        "💡 Cocok untuk Scalping & Intraday\n"
        "📈 Support: EURUSD M1/M5\n\n"
        "💰 Harga: <b>Rp 199.000</b>"
    )
    await callback.message.edit_text(text, reply_markup=InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="🔙 Kembali", callback_data="menu")]]
    ))

# 💳 METODE PEMBAYARAN
@dp.callback_query(F.data == "buy")
async def callback_buy(callback: types.CallbackQuery):
    text = "💳 <b>Pilih Metode Pembayaran:</b>"
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏦 Rekening Bank (BCA)", callback_data="pay_bank")],
        [InlineKeyboardButton(text="📱 E-Wallet & Crypto", callback_data="pay_ewallet")],
        [InlineKeyboardButton(text="🔙 Kembali", callback_data="menu")]
    ])
    await callback.message.edit_text(text, reply_markup=keyboard)

# BANK
@dp.callback_query(F.data == "pay_bank")
async def pay_bank(callback: types.CallbackQuery):
    text = (
        "🏦 <b>Pembayaran via Bank BCA:</b>\n\n"
        "Nama: ROHIM SOFIYAN\n"
        "No. Rek: <code>5411303072</code>\n\n"
        "📤 Setelah transfer, upload bukti pembayaran."
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📤 Upload Bukti Pembayaran", callback_data="upload_proof")],
        [InlineKeyboardButton(text="🔙 Kembali", callback_data="buy")]
    ])
    await callback.message.edit_text(text, reply_markup=keyboard)

# CRYPTO + DANA
@dp.callback_query(F.data == "pay_ewallet")
async def pay_ewallet(callback: types.CallbackQuery):
    text = (
        "📱 <b>Pembayaran E-Wallet & Crypto:</b>\n\n"
        "<b>DANA</b>\n"
        "📲 085692697242 a.n. ROHIM SOFIYAN\n\n"
        "<b>Crypto</b>\n"
        "🔹 <b>SOLANA</b>: <code>HmbBk8fhbu8qPExuCawxAScGqpeSHm6XkdTmqhaQX3sW</code>\n"
        "🔹 <b>BTC</b>: <code>bc1qw68622xht3qurkhgn8qg2jf4hz09vjcrs9jhs3</code>\n"
        "🔹 <b>ETH</b>: <code>0x146C8b20961566683Aa278c8B217f4b0e4930bFa</code>\n\n"
        "📤 Setelah transfer, upload bukti pembayaran."
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📤 Upload Bukti Pembayaran", callback_data="upload_proof")],
        [InlineKeyboardButton(text="🔙 Kembali", callback_data="buy")]
    ])
    await callback.message.edit_text(text, reply_markup=keyboard)

# 📤 UPLOAD BUKTI
@dp.callback_query(F.data == "upload_proof")
async def callback_upload(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("📤 Silakan kirim foto bukti pembayaran sekarang.")
    await state.set_state(PurchaseForm.uploading_proof)

# HANDLE FOTO PEMBAYARAN
@dp.message(PurchaseForm.uploading_proof, F.photo)
async def handle_proof(message: Message, state: FSMContext):
    user = message.from_user
    device = platform.system()
    info = (
        f"🧾 <b>Bukti Pembayaran Masuk</b>\n\n"
        f"👤 Username: @{user.username or '-'}\n"
        f"🆔 User ID: <code>{user.id}</code>\n"
        f"💻 Device: {device}\n"
        f"🌐 Jaringan: {message.chat.type}\n"
        f"📎 Bukti terlampir di bawah."
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Konfirmasi Pembayaran", callback_data=f"confirm_{user.id}")]
    ])
    photo = message.photo[-1]
    await bot.send_photo(chat_id=ADMIN_ID, photo=photo.file_id, caption=info, reply_markup=keyboard)

    await message.answer("✅ Bukti pembayaran kamu sudah dikirim ke admin. Mohon tunggu 2–5 menit.")
    await state.clear()

# ✅ KONFIRMASI ADMIN
@dp.callback_query(F.data.startswith("confirm_"))
async def confirm_payment(callback: types.CallbackQuery):
    user_id = int(callback.data.split("_")[1])
    await bot.send_message(chat_id=user_id, text=(
        f"✅ <b>Pembayaran kamu telah dikonfirmasi!</b>\n"
        f"🔗 Silakan join ke channel eksklusif:\n{CHANNEL_LINK}"
    ))
    await callback.message.edit_text("✅ Pembayaran dikonfirmasi. Link sudah dikirim ke pembeli.")

# BANTUAN
@dp.callback_query(F.data == "help")
async def help_callback(callback: types.CallbackQuery):
    text = (
        "🆘 <b>Bantuan:</b>\n\n"
        "📌 Gunakan /start atau /menu untuk melihat produk.\n"
        "📤 Upload bukti setelah transfer.\n"
        "⏳ Tunggu admin konfirmasi dalam 2–5 menit.\n\n"
        "❓ Masalah lain? Klik tombol chat admin."
    )
    await callback.message.edit_text(text, reply_markup=InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="💬 Chat Admin", url="https://t.me/NOBITA_291200")]]
    ))

# 💬 /chat_admin
@dp.message(F.text == "/chat_admin")
async def chat_admin(message: types.Message):
    await message.answer("💬 Hubungi admin di sini: @NOBITA_291200")

# 🔁 Kembali ke menu
@dp.callback_query(F.data == "menu")
async def back_to_menu(callback: types.CallbackQuery):
    await cmd_menu(callback.message)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(dp.start_polling(bot))
