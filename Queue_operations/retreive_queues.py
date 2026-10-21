from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from db.get_queues import get_user_queues

async def list_queues(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    queues = get_user_queues(user_id)

    if not queues:
        await update.message.reply_text("You have no queues. Create one with /createQueue <name>.")
        return

    buttons = []
    for queue_id, name in queues:
        buttons.append([
            InlineKeyboardButton(name, callback_data=f"showqueue:{queue_id}"),
            InlineKeyboardButton("🗑️", callback_data=f"delqueue:{queue_id}"),
        ])
    keyboard = InlineKeyboardMarkup(buttons)

    await update.message.reply_text("📂 Your queues:", reply_markup=keyboard)