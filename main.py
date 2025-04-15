from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.webhook.aiohttp_server import setup_application
from aiohttp import web
import asyncio
import os

from handle import router  # Router kamu

BOT_TOKEN = "7830689776:AAFJabHa7QdnuKfz0b97N8x5TGsl9RPPBX0"
WEBHOOK_URL = "https://3b9b7b70-5a04-4a49-aed2-672bb9746dfb-00-14gue8bn4vxxr.pike.replit.dev"  # ganti domainnya

async def on_startup(bot: Bot):
    await bot.set_webhook(WEBHOOK_URL)

async def main():
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)

    app = web.Application()
    app["bot"] = bot
    dp.startup.register(on_startup)
    setup_application(app, dp, bot=bot)


    return app

if __name__ == "__main__":
    web.run_app(main(), port=int(os.environ.get("PORT", 8000)))
