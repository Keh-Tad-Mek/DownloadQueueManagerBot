import os
from telegram import Update
from telegram.ext import Application
from telegram.ext import CommandHandler
from telegram.ext import ContextTypes
from telegram.ext import MessageHandler
from telegram.ext import filters
from telegram.ext import CallbackQueryHandler
from dotenv import load_dotenv
from Handle_file.handle_file import handle_file
from Handle_file.button_handlers import handle_add_to_queue, choose_queue, handle_delete_queue
from Queue_operations.retreive_queues import list_queues
from Queue_operations.create_queue import create_queue


load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome"
    )

    
def main():
    # tells the server to listen to the bot that has this token
    app = Application.builder().token(TOKEN).build()

    print("Bot is running.....")

    file_filter = filters.Document.ALL | filters.VIDEO | filters.AUDIO | filters.VOICE | filters.VIDEO_NOTE | filters.ANIMATION
    # all the commands that the bot can handle are added here
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("createQueue", create_queue))
    app.add_handler(CommandHandler("listQueues", list_queues))
    app.add_handler(MessageHandler(file_filter, handle_file))
    app.add_handler(CallbackQueryHandler(handle_add_to_queue, pattern="^add:"))
    app.add_handler(CallbackQueryHandler(choose_queue, pattern="^pickQueue:"))
    app.add_handler(CallbackQueryHandler(handle_delete_queue, pattern="^delqueue:"))


    # tells the bot to start polling for updates from Telegram
    app.run_polling()

if __name__ == "__main__":
    main()