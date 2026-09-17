import os
from telegram import Update
from telegram.ext import ContextTypes   
from Handle_file.file_metadata_handler import get_file_from_message, format_file_info    

async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    label, file_obj = get_file_from_message(message)

    if not file_obj:
        await message.reply_text("Unknown file type.")
        return

    response = format_file_info(label, file_obj)
    await message.reply_text(response, parse_mode="Markdown")