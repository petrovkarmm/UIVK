from aiogram.types import Message
from aiogram_dialog import DialogManager


async def new_faq_file_input(message: Message, _message_input, dialog_manager: DialogManager):
    if message.from_user.is_bot:
        return

    file_data = dialog_manager.dialog_data.get("new_faq_file")

    # Определяем тип и file_id
    if message.photo:
        ftype = "photo"
        file_id = message.photo[-1].file_id
    elif message.video:
        ftype = "video"
        file_id = message.video.file_id
    elif message.document:
        ftype = "document"
        file_id = message.document.file_id
    else:
        await message.answer("❌ Можно загружать только фото, видео или документы.")
        return

    # Проверяем ограничение: только 1 файл
    if file_data:
        await message.answer("❌ Уже есть файл, сначала очистите его через кнопку «Очистить».")
        return

    # Сохраняем файл
    dialog_manager.dialog_data["new_faq_file"] = {"file_id": file_id, "type": ftype}
    await message.answer(f"✅ Файл {ftype} добавлен.")

