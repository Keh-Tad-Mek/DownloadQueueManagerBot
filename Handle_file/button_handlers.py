from telegram import Update
from telegram.ext import ContextTypes  
from db.get_queues import get_user_queues
from db.add_to_queues import add_to_queue
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


async def choose_queue(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    _, token, queue_id = query.data.split(":")

    file_obj = context.user_data.get("pending_files", {}).get(token)

    if not file_obj:
        return await query.edit_message_text("This file is no longer available.")
    
    file_id = file_obj.file_id

    result, message = add_to_queue(queue_id, file_id)

    return await query.edit_message_text(message)

    



async def handle_add_to_queue(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    token = query.data.split(":", 1)[1]
    file_obj = context.user_data.get("pending_files", {}).get(token)

    if not file_obj:
        await query.edit_message_text("This file is no longer available. Resend it to the bot to add it to your queue.")
        return 

    user_id = query.from_user.id

    queues = get_user_queues(user_id)

    if not queues:
        await query.edit_message_text("You have no queues. Create one with /createQueue <queueName>.")
        return

    buttons = [
        [InlineKeyboardButton(name, callback_data=f"pickQueue:{token}:{queue_id}")]
        for queue_id, name in queues
    ]

    keyboard = InlineKeyboardMarkup(buttons)

    await query.edit_message_text("Choose a queue:", reply_markup=keyboard)
