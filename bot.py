import os
from telegram import Update
from telegram.ext import Application
from telegram.ext import CommandHandler
from telegram.ext import ContextTypes
from telegram.ext import MessageHandler
from telegram.ext import filters
from dotenv import load_dotenv
from file_handler import get_file_from_message, format_file_info
from utils.validate_queue_name import name_is_valid

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome"
    )


async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    label, file_obj = get_file_from_message(message)

    if not file_obj:
        await message.reply_text("Unknown file type.")
        return

    response = format_file_info(label, file_obj)
    await message.reply_text(response, parse_mode="Markdown")


async def create_queue(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return
    
    if not context.args:
        await update.message.reply_text("Please provide a name for your queue. \n" \
        "Usage: /createQueue <queue_name>")

    if len(context.args) > 1:
        await update.message.reply_text("No spaces allowed in queue name. \n" \
                    "Only letters, numbers, and underscores are allowed. \n" \
                    "Usage: /createQueue <queue_name>")


    queue_name = context.args[0]

    is_valid, message = name_is_valid(queue_name)
    
    if not is_valid:
        await update.message.reply_text(message)
        return


    
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