import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome"
    )

def main():
    # tells the server to listen to the bot that has this token
    app = Application.builder().token(TOKEN).build()

    # all the commands that the bot can handle are added here
    
    app.add_handler(CommandHandler("start", start))

    # tells the bot to start polling for updates from Telegram
    app.run_polling()

if __name__ == "__main__":
    main()