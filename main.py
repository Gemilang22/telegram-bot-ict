import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Router

API_TOKEN = "7314074107:AAHRk9CiM1U0fuEgtlNxQDPk5ksKgfHFf2g"

router = Router()

@router.message(commands=["start"])
async def cmd_start(message: Message):
    await message.answer("Welcome to the bot!")

async def main():
    bot = Bot(token=API_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
