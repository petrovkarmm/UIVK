from aiogram_dialog import DialogManager

async def new_faq_file_getter(dialog_manager: DialogManager, **kwargs):
    file_data = dialog_manager.dialog_data.get("new_faq_file")
    return {
        "has_file": bool(file_data),
        "file_type": file_data["type"] if file_data else "",
        "file_count": "1/1" if file_data else "0/1"
    }
