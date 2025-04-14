import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor

API_TOKEN = '7830689776:AAFJabHa7QdnuKfz0b97N8x5TGsl9RPPBX0'

# Set up logging
logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Register a message handler
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Welcome to the bot!")

# This function runs the bot
async def on_start():
    await dp.start_polling()

if __name__ == '__main__':
    # Start the bot
    executor.start_polling(dp, skip_updates=True)
