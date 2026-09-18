import os
from telegram import Update
from telegram.ext import ContextTypes
from Queue_creation.validate_queue_name import name_is_valid
from Queue_creation.register_queue import register_queue

async def create_queue(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

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


    success, message = register_queue(queue_name, user_id)

    if success:
        await update.message.reply_text(message)
    else:
        await update.message.reply_text(message)