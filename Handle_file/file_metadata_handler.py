from telegram import Message 
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

FILE_TYPES = {
    "document": ("Document", lambda m: m.document),
    "video":    ("Video",    lambda m: m.video),
    "audio":    ("Audio",    lambda m: m.audio),
    "photo":    ("Photo",    lambda m: m.photo[-1] if m.photo else None),
}

def get_file_from_message(message: Message):
    for label, getter in FILE_TYPES.values():
        file_obj = getter(message)

        if file_obj:
            return label, file_obj

    return None, None

def format_file_info(label: str, file_obj):
    response = ""
    if hasattr(file_obj, "file_name") and file_obj.file_name:
        response += f"📁 `{file_obj.file_name}` \n"


    return response