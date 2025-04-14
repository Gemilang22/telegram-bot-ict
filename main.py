import logging
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode  # Perubahan di sini
from aiogram.utils import executor
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from handlers import register_handlers

# ======= Konfigurasi Logging =======
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ======= Inisialisasi Bot dan Dispatcher =======
API_TOKEN = "7830689776:AAFJabHa7QdnuKfz0b97N8x5TGsl9RPPBX0"  # Ganti dengan token bot Telegram Anda
bot = Bot(token=API_TOKEN, parse_mode=ParseMode.HTML)
storage = MemoryStorage()  # Penyimpanan status FSM di memory
dp = Dispatcher(bot, storage=storage)

# ======= Registrasi Handlers =======
register_handlers(dp.router)

# ======= Main Program =======
async def on_start(message: types.Message):
    await message.answer("Bot telah berhasil dijalankan!")

async def on_shutdown(dp):
    logging.warning("Shutting down..")
    await dp.storage.close()
    await dp.storage.wait_closed()

if __name__ == '__main__':
    # Menjalankan bot
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True, on_start=on_start, on_shutdown=on_shutdown)
