import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.types import (
    Message, InlineKeyboardMarkup, InlineKeyboardButton,
    CallbackQuery, FSInputFile, InputFile
)
from aiogram.filters import Command
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

# 🔐 TOKEN BOT
API_TOKEN = "7830689776:AAFJabHa7QdnuKfz0b97N8x5TGsl9RPPBX0"

# 🤖 Setup Bot & Dispatcher
bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())

# 🚥 FSM STATES
class PurchaseForm(StatesGroup):
    choosing_version = State()
    filling_name = State()
    filling_contact = State()
    choosing_payment = State()
    adding_notes = State()
    uploading_proof = State()

# 🧾 MENU UTAMA
def main_menu():
    return InlineKeyboardMarkup(inline_keyboard=[  
        [InlineKeyboardButton(text="🛒 Info EA & Beli EA", callback_data="info_ea")],
        [InlineKeyboardButton(text="📘 Panduan Pasang EA", callback_data="install_guide")],
        [InlineKeyboardButton(text="🧠 Tentang Strategi ICT", callback_data="ict_strategy")],
        [InlineKeyboardButton(text="📞 Kontak Admin", url="https://t.me/NOBITA_291200")],
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
        "📁 File > Open Data Folder\n➡️ MQL5 > Experts\n📌 Paste file EA di folder tersebut\n"
        "🔄 Restart MT5 dan buka Navigator\n📊 Tarik EA ke chart dan centang Allow DLL & Auto Trading\n\n"
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
        "✔️ Break of Structure (BOS)\n✔️ Order Block (OB)\n✔️ Fair Value Gap (FVG)\n\n"
        "EA kami fokus pada entry otomatis di TF kecil (M1–M15) menggunakan sinyal-sinyal ini.\n"
        "Cocok untuk scalping dengan winrate optimal! 🚀",
        reply_markup=back_menu()
    )
    await callback.answer()

# 🛒 Info EA
@dp.callback_query(lambda c: c.data == "info_ea")
async def info_ea(callback: CallbackQuery, state: FSMContext):
    markup = InlineKeyboardMarkup(inline_keyboard=[  
        [InlineKeyboardButton(text="🛒 Beli EA Ini", callback_data="buy_ea")],
        [InlineKeyboardButton(text="⬅️ Kembali ke Menu", callback_data="back_to_menu")]
    ])
    await callback.message.edit_text(
        "<b>🛠 INFO PRODUK: EA ICT BY NOBITA</b>\n\n"
        "<b>Versi 1:</b> EA_ICT_SNR_By Nobita_v1 - <b>Harga: Rp 300,000</b>\n"
        "• Risk Management\n• Lot 0.01–0.03\n• Check News + Auto Close\n• Full ICT: BOS + FVG + OB + Candle\n• Smart SL/TP + Breakeven + Trailing Stop\n\n"
        "<b>Versi 2:</b> EA_ICT_SNR_By Nobita_v2 - <b>Harga: Rp 150,000</b>\n"
        "• Risk Management\n• Lot 0.01 fix\n• Strategi: Candle Pattern + SNR\n\n"
        "<b>Versi 3:</b> EA_ICT_SNR_By Nobita_v3 - <b>Harga: Rp 100,000</b>\n"
        "• No Risk Management\n• Lot 0.01 fix\n• Strategi: SNR saja",
        reply_markup=markup
    )
    await callback.answer()

# ➡️ Step Beli EA
@dp.callback_query(lambda c: c.data == "buy_ea")
async def choose_version(callback: CallbackQuery, state: FSMContext):
    markup = InlineKeyboardMarkup(inline_keyboard=[  
        [InlineKeyboardButton(text="Versi 1", callback_data="v1"),
         InlineKeyboardButton(text="Versi 2", callback_data="v2"),
         InlineKeyboardButton(text="Versi 3", callback_data="v3")],
        [InlineKeyboardButton(text="❌ Batalkan", callback_data="cancel_tx")]
    ])
    await callback.message.edit_text("Pilih versi EA yang ingin kamu beli:", reply_markup=markup)
    await state.set_state(PurchaseForm.choosing_version)

@dp.callback_query(lambda c: c.data in ["v1", "v2", "v3"])
async def save_version(callback: CallbackQuery, state: FSMContext):
    await state.update_data(version=callback.data)
    await callback.message.answer("Masukkan nama lengkap kamu:", reply_markup=cancel_button())
    await state.set_state(PurchaseForm.filling_name)

@dp.message(PurchaseForm.filling_name)
async def fill_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Masukkan nomor WhatsApp atau Telegram kamu:", reply_markup=cancel_button())
    await state.set_state(PurchaseForm.filling_contact)

@dp.message(PurchaseForm.filling_contact)
async def fill_contact(message: Message, state: FSMContext):
    await state.update_data(contact=message.text)
    markup = InlineKeyboardMarkup(inline_keyboard=[  
        [InlineKeyboardButton(text="BANK BCA", callback_data="pay_bank"),
         InlineKeyboardButton(text="DANA", callback_data="pay_dana"),
         InlineKeyboardButton(text="Solana (SOL)", callback_data="pay_solana"),
         InlineKeyboardButton(text="Bitcoin (BTC)", callback_data="pay_btc"),
         InlineKeyboardButton(text="Ethereum (ETH)", callback_data="pay_eth")],
        [InlineKeyboardButton(text="❌ Batalkan", callback_data="cancel_tx")]
    ])
    await message.answer("Pilih metode pembayaran:", reply_markup=markup)
    await state.set_state(PurchaseForm.choosing_payment)

@dp.callback_query(lambda c: c.data.startswith("pay_"))
async def save_payment(callback: CallbackQuery, state: FSMContext):
    method = callback.data.replace("pay_", "")
    await state.update_data(payment_method=method)

    payment_text = {
        "bank": "BANK BCA\nNo: 5411303072\nA/N: ROHIM SOFIYAN",
        "dana": "DANA: 085692697242 (a.n ROHIM SOFIYAN)",
        "solana": "Solana Wallet: 5NVt5tKx46p5rpH5wFVFGoD4Vmua1gR7A3mbmfPSRVR8",
        "btc": "Bitcoin Wallet: 1A2b3C4D5e6F7G8H9J0kL",
        "eth": "Ethereum Wallet: 0x5F3AB5b742Fd8d2744DBeC0fEc2Bb8A9F6F2e9C1"
    }

    await callback.message.answer(f"Detail Pembayaran:\n<pre>{payment_text[method]}</pre>\n\nTulis keterangan tambahan (jika ada), atau ketik - jika tidak ada:", parse_mode="HTML", reply_markup=cancel_button())
    await state.set_state(PurchaseForm.adding_notes)

@dp.message(PurchaseForm.adding_notes)
async def fill_notes(message: Message, state: FSMContext):
    await state.update_data(notes=message.text)
    await message.answer("Silakan kirim bukti pembayaran (gambar):", reply_markup=cancel_button())
    await state.set_state(PurchaseForm.uploading_proof)

@dp.message(PurchaseForm.uploading_proof, content_types=types.ContentType.PHOTO)
async def receive_proof(message: Message, state: FSMContext):
    if not message.photo:
        await message.answer("❗ Kirim bukti dalam bentuk foto.")
        return
    photo = message.photo[-1]
    file_id = photo.file_id
    data = await state.get_data()

    await bot.send_photo(
        chat_id="@NOBITA_291200",
        photo=file_id,
        caption=f"📥 Pembelian EA Baru:\n\n"
                f"👤 Nama: {data['name']}\n☎️ Kontak: {data['contact']}\n💼 Versi: {data['version']}\n💰 Metode: {data['payment_method']}\n📝 Catatan: {data['notes']}"
    )

    await message.answer("✅ Bukti pembayaran diterima. Admin akan menghubungi kamu segera. Terima kasih!")
    await state.clear()

# ❌ Cancel
@dp.callback_query(lambda c: c.data == "cancel_tx")
async def cancel_transaction(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer("❌ Transaksi dibatalkan. Kamu bisa mulai lagi dengan perintah /menu.")
    await callback.answer()

def cancel_button():
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="❌ Batalkan", callback_data="cancel_tx")]])

if __name__ == "__main__":
    asyncio.run(main())
