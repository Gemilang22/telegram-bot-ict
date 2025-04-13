from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

# /menu handler
@dp.message(Command("menu"))
async def menu_handler(message: Message):
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(text="📥 Download EA", callback_data="download"),
        InlineKeyboardButton(text="📊 Cek Sinyal Hari Ini", callback_data="signal")
    )
    builder.row(
        InlineKeyboardButton(text="🔔 Aktifkan Notifikasi", callback_data="notif"),
        InlineKeyboardButton(text="📘 Panduan EA", callback_data="guide")
    )
    builder.row(
        InlineKeyboardButton(text="🧠 Strategi ICT", callback_data="strategy"),
        InlineKeyboardButton(text="🛠 Kontak Admin", url="https://t.me/username_admin_kamu")
    )

    await message.answer(
        "<b>📋 Menu Interaktif EA ICT</b>\nPilih opsi di bawah ini untuk melanjutkan:",
        reply_markup=builder.as_markup()
    )

# Callback handler
@dp.callback_query()
async def callback_handler(callback_query: types.CallbackQuery):
    data = callback_query.data

    if data == "guide":
        await callback_query.message.edit_text(
            "<b>📘 Panduan Pemasangan EA:</b>\n\n"
            "1️⃣ Buka MT5 ➤ File ➤ Open Data Folder\n"
            "2️⃣ Masuk ke MQL5 ➤ Experts\n"
            "3️⃣ Copy file EA (.ex5) ke sana\n"
            "4️⃣ Restart MT5 dan buka Navigator (Ctrl+N)\n"
            "5️⃣ Drag EA ke chart & aktifkan AutoTrading\n\n"
            "🛡 Gunakan akun demo dulu untuk testing."
        )
    elif data == "strategy":
        await callback_query.message.edit_text(
            "<b>🧠 Strategi ICT (Inner Circle Trader)</b>\n\n"
            "✅ Break of Structure (BOS)\n"
            "✅ Fair Value Gap (FVG)\n"
            "✅ Order Block (OB)\n\n"
            "📌 Digunakan untuk entry berbasis retest zona likuiditas.\n"
            "⚡ Cocok untuk scalping di TF M1–M15."
        )
    elif data == "download":
        await callback_query.message.edit_text(
            "<b>📥 Download EA ICT</b>\n\n"
            "Silakan unduh EA terbaru melalui link berikut:\n"
            "🔗 <a href='https://example.com/ea-download-link'>Download EA ICT by Nobita</a>\n\n"
            "📦 Pastikan gunakan file dengan ekstensi `.ex5`!"
        )
    elif data == "signal":
        await callback_query.message.edit_text(
            "<b>📊 Sinyal Hari Ini:</b>\n\n"
            "• EURUSD ➤ BUY (Support OB 1.0700)\n"
            "• XAUUSD ➤ SELL (FVG 2350.50)\n"
            "• BTCUSD ➤ WAIT (No setup yet)\n\n"
            "📅 Update terakhir: Otomatis harian."
        )
    elif data == "notif":
        await callback_query.message.edit_text(
            "<b>🔔 Notifikasi Aktif</b>\n\n"
            "Kamu akan mendapatkan notifikasi:\n"
            "• Saat EA aktif\n"
            "• Saat Entry, TP, atau SL\n\n"
            "📲 Pastikan Telegram kamu terhubung!"
        )

    await callback_query.answer()
