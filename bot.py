import os
from telegram import Update
from telegram.ext import Application
from telegram.ext import CommandHandler
from telegram.ext import ContextTypes
from telegram.ext import MessageHandler
from telegram.ext import filters
from dotenv import load_dotenv
from Handle_file.handle_file import handle_file
from Queue_creation.create_queue import create_queue

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome"
    )


    
def main():
    # tells the server to listen to the bot that has this token
    app = Application.builder().token(TOKEN).build()

    file_filter = filters.Document.ALL | filters.VIDEO | filters.AUDIO | filters.VOICE | filters.VIDEO_NOTE | filters.ANIMATION
    # all the commands that the bot can handle are added here
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("createQueue", create_queue))
    app.add_handler(MessageHandler(file_filter, handle_file))

    # tells the bot to start polling for updates from Telegram
    app.run_polling()

if __name__ == "__main__":
    main()