from telegram import Message 

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
    response = f"{label} detected! \n"
    response += f"ID: `{file_obj.file_id}` \n"

    if hasattr(file_obj, "file_name") and file_obj.file_name:
        response += f"Name: `{file_obj.file_name}` \n"

    if hasattr(file_obj, "file_size") and file_obj.file_size:
        response += f"Size: `{file_obj.file_size}` bytes \n"

    return response