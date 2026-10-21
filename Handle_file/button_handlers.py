from telegram import Update
from telegram.ext import ContextTypes  
from db.get_queues import get_user_queues
from db.add_to_queues import add_to_queue
from db.remove_queues import delete_queue
from db.get_queue_items import get_queue_items
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


async def handle_show_queue(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    queue_id = int(query.data.split(":")[1])
    # Fetch items for this queue from your DB
    items = get_queue_items(queue_id) 

    if not items:
        await query.edit_message_text("This queue is empty.")
        return

    await query.edit_message_text(f"Sending {len(items)} items...")
    
    for item_id, file_id, position, status in items:
        # This sends the file using the file_id
        await context.bot.send_document(chat_id=query.message.chat_id, document=file_id.strip())


async def handle_delete_queue(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    queue_id = int(query.data.split(":")[1])
    user_id = query.from_user.id

    success, message = delete_queue(queue_id, user_id)

    if not success:
        await query.answer(message, show_alert=True)
        return

    # re-fetch remaining queues and re-render the keyboard
    queues = get_user_queues(user_id)

    if not queues:
        await query.edit_message_text("You have no queues. Create one with /createQueue <name>.")
        return

    buttons = []
    for qid, name in queues:
        buttons.append([
            InlineKeyboardButton(name, callback_data=f"showqueue:{qid}"),
            InlineKeyboardButton("🗑️", callback_data=f"delqueue:{qid}"),
        ])

    keyboard = InlineKeyboardMarkup(buttons)

    await query.edit_message_text("📂 Your queues:", reply_markup=keyboard)


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
