from aiogram import types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import Bot
from aiogram.filters import Command
from aiogram.dispatcher.router import Router

# ======= FSM STATES =======
class PurchaseForm(StatesGroup):
    choosing_version = State()
    filling_name = State()
    filling_contact = State()
    choosing_payment = State()
    adding_notes = State()
    uploading_proof = State()

# ======= INLINE BUTTONS =======
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

def cancel_button():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="❌ Batalkan", callback_data="cancel_tx")]
    ])

# ======= HANDLERS =======
def register_handlers(router: Router):

    @router.message(Command("start"))
    async def start_handler(message: types.Message):
        await message.answer(
            "<b>👋 Selamat datang di EA ICT by Nobita</b>\n\n"
            "Bot ini akan membantu kamu:\n"
            "• 📘 Memasang EA di MT5\n"
            "• 🧠 Mengenal strategi ICT\n"
            "• 🔔 Menerima sinyal dan notifikasi\n\n"
            "Gunakan perintah /menu untuk mulai 🚀",
            reply_markup=main_menu()
        )

    @router.message(Command("menu"))
    async def menu_handler(message: types.Message):
        await message.answer("<b>📋 MENU UTAMA</b>\nSilakan pilih menu di bawah ini 👇", reply_markup=main_menu())

    @router.callback_query(lambda c: c.data == "back_to_menu")
    async def back_to_menu(callback: CallbackQuery):
        await callback.message.edit_text("<b>📋 MENU UTAMA</b>\nSilakan pilih menu di bawah ini 👇", reply_markup=main_menu())
        await callback.answer()

    @router.callback_query(lambda c: c.data == "install_guide")
    async def install_guide(callback: CallbackQuery):
        await callback.message.edit_text(
            "<b>📘 Cara Install EA di MetaTrader 5 (PC)</b>\n\n"
            "📁 File > Open Data Folder\n➡️ MQL5 > Experts\n📌 Paste file EA di folder tersebut\n"
            "🔄 Restart MT5 dan buka Navigator\n📊 Tarik EA ke chart dan centang Allow DLL & Auto Trading\n\n"
            "🟢 Siap! Gunakan VPS agar trading 24 jam nonstop.",
            reply_markup=back_menu()
        )
        await callback.answer()

    @router.callback_query(lambda c: c.data == "ict_strategy")
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

    @router.callback_query(lambda c: c.data == "info_ea")
    async def info_ea(callback: CallbackQuery, state: FSMContext):
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🛒 Beli EA Ini", callback_data="buy_ea")],
            [InlineKeyboardButton(text="⬅️ Kembali ke Menu", callback_data="back_to_menu")]
        ])
        await callback.message.edit_text(
            "<b>🛠 INFO PRODUK: EA ICT BY NOBITA</b>\n\n"
            "<b>Versi 1:</b> EA_ICT_SNR_By Nobita_v1 - <b>Harga: Rp 300,000</b>\n"
            "• Risk Management\n• Lot 0.01–0.03\n• Check News + Auto Close\n• Full ICT: BOS + FVG + OB + Candle\n"
            "• Smart SL/TP + Breakeven + Trailing Stop\n\n"
            "<b>Versi 2:</b> EA_ICT_SNR_By Nobita_v2 - <b>Harga: Rp 150,000</b>\n"
            "• Risk Management\n• Lot 0.01 fix\n• Strategi: Candle Pattern + SNR\n\n"
            "<b>Versi 3:</b> EA_ICT_SNR_By Nobita_v3 - <b>Harga: Rp 100,000</b>\n"
            "• No Risk Management\n• Lot 0.01 fix\n• Strategi: SNR saja",
            reply_markup=markup
        )
        await callback.answer()

    @router.callback_query(lambda c: c.data == "buy_ea")
    async def choose_version(callback: CallbackQuery, state: FSMContext):
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Versi 1", callback_data="v1"),
             InlineKeyboardButton(text="Versi 2", callback_data="v2"),
             InlineKeyboardButton(text="Versi 3", callback_data="v3")],
            [InlineKeyboardButton(text="❌ Batalkan", callback_data="cancel_tx")]
        ])
        await callback.message.edit_text("Pilih versi EA yang ingin kamu beli:", reply_markup=markup)
        await state.set_state(PurchaseForm.choosing_version)

    @router.callback_query(lambda c: c.data in ["v1", "v2", "v3"])
    async def save_version(callback: CallbackQuery, state: FSMContext):
        await state.update_data(version=callback.data)
        await callback.message.answer("Masukkan nama lengkap kamu:", reply_markup=cancel_button())
        await state.set_state(PurchaseForm.filling_name)

    @router.message(PurchaseForm.filling_name)
    async def fill_name(message: types.Message, state: FSMContext):
        await state.update_data(name=message.text)
        await message.answer("Masukkan nomor WhatsApp atau Telegram kamu:", reply_markup=cancel_button())
        await state.set_state(PurchaseForm.filling_contact)

    @router.message(PurchaseForm.filling_contact)
    async def fill_contact(message: types.Message, state: FSMContext):
        await state.update_data(contact=message.text)
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="BANK BCA", callback_data="pay_bank"),
             InlineKeyboardButton(text="DANA", callback_data="pay_dana")],
            [InlineKeyboardButton(text="Solana (SOL)", callback_data="pay_solana"),
             InlineKeyboardButton(text="Bitcoin (BTC)", callback_data="pay_btc"),
             InlineKeyboardButton(text="Ethereum (ETH)", callback_data="pay_eth")],
            [InlineKeyboardButton(text="❌ Batalkan", callback_data="cancel_tx")]
        ])
        await message.answer("Pilih metode pembayaran:", reply_markup=markup)
        await state.set_state(PurchaseForm.choosing_payment)

    @router.callback_query(lambda c: c.data.startswith("pay_"))
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

        await callback.message.answer(
            f"Detail Pembayaran:\n<pre>{payment_text[method]}</pre>\n\n"
            "Tulis keterangan tambahan (jika ada), atau ketik - jika tidak ada:",
            parse_mode="HTML", reply_markup=cancel_button()
        )
        await state.set_state(PurchaseForm.adding_notes)

    @router.message(PurchaseForm.adding_notes)
    async def fill_notes(message: types.Message, state: FSMContext):
        await state.update_data(notes=message.text)
        await message.answer("Silakan kirim bukti pembayaran (gambar):", reply_markup=cancel_button())
        await state.set_state(PurchaseForm.uploading_proof)

    @router.message(PurchaseForm.uploading_proof, F.photo)
    async def receive_proof(message: types.Message, state: FSMContext, bot: Bot):
        photo = message.photo[-1]
        file_id = photo.file_id
        data = await state.get_data()

        print(f"DEBUG: file_id: {file_id}")
        print(f"DEBUG: data: {data}")

        try:
            await bot.send_photo(
                chat_id=8081196747,
                photo=file_id,
                caption=(f"📥 Pembelian EA Baru:\n\n"
                         f"Nama: {data['name']}\n"
                         f"Kontak: {data['contact']}\n"
                         f"Versi: {data['version']}\n"
                         f"Pembayaran via: {data['payment_method']}\n"
                         f"Keterangan: {data.get('notes', '-')}")
            )
            await message.answer("Terima kasih! Bukti pembayaran diterima. Admin akan segera memproses pesanan Anda.")
            await state.clear()

        except Exception as e:
            await message.answer(f"Terjadi kesalahan: {str(e)}")

    @router.callback_query(lambda c: c.data == "cancel_tx")
    async def cancel_transaction(callback: CallbackQuery, state: FSMContext):
        await state.clear()
        await callback.answer("Transaksi dibatalkan.", show_alert=True)
        await callback.message.edit_text("Pembelian dibatalkan. Untuk memulai ulang, ketik /menu")
        await callback.answer()

# Example of how to register the handler
router = Router()
register_handlers(router)
