# main.py

from aiogram import Dispatcher, Bot
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties

from handle import router  # ⬅️ INI WAJIB

async def main():
    bot = Bot(token="7314074107:AAHRk9CiM1U0fuEgtlNxQDPk5ksKgfHFf2g", default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(router)  # ⬅️ PASTIKAN INI ADA

    await dp.start_polling(bot)
