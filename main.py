import os
from handlers import setup_handlers
from telegram.ext import ApplicationBuilder

TOKEN = os.getenv("BOT_TOKEN")  # ambil token dari env

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    setup_handlers(app)
    print("Bot is running on Railway...")
    app.run_polling()

if __name__ == '__main__':
    main()
