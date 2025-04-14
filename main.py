import asyncio
from aiogram import Bot, Dispatcher, Router
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command

API_TOKEN = "7314074107:AAHRk9CiM1U0fuEgtlNxQDPk5ksKgfHFf2g"  # Ganti dengan token asli

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Selamat datang di bot!")

async def main():
    bot = Bot(
        token=API_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
