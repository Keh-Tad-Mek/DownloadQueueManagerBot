import os
from telegram import Update
from telegram.ext import ContextTypes   
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from Handle_file.file_metadata_handler import get_file_from_message, format_file_info    

async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    media_group_id = message.media_group_id
    print(media_group_id)

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Add all to a single queue",
        callback_data=f"addall:{media_group_id}")]
    ])

    if not media_group_id:
        pass

    elif not context.user_data.get('last_media_group_id'):
        context.user_data['last_media_group_id'] = media_group_id
        await message.reply_text("Choose what to do with these items:",
        reply_markup=keyboard)

    elif context.user_data.get('last_media_group_id') != media_group_id:
        context.user_data['last_media_group_id'] = media_group_id
        await message.reply_text("Choose what to do with these items:",
        reply_markup=keyboard)

    elif context.user_data.get('last_media_group_id') == media_group_id:
        pass


    label, file_obj = get_file_from_message(message)

    if not file_obj:
        await message.reply_text("Unknown file type.")
        return

    response = format_file_info(label, file_obj)
    await message.reply_text(response, parse_mode="Markdown")