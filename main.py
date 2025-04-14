import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from handle import router  # Router kamu dari file handle.py

# Ganti dengan token bot kamu
BOT_TOKEN = "7314074107:AAHRk9CiM1U0fuEgtlNxQDPk5ksKgfHFf2g"

async def main():
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)  # Pastikan router sudah di-import dari handle.py

    print("🤖 Bot berhasil dijalankan...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
