from aiogram.enums import ContentType
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import MediaAttachment, MediaId

from src.database.dataclasses.vacancy import Vacancy
from src.logs.logger import bot_logger


async def new_faq_answer_and_question_getter(dialog_manager: DialogManager, **_kwargs):
    new_faq_question = dialog_manager.dialog_data.get('new_faq_question', '')
    new_faq_answer = dialog_manager.dialog_data.get('new_faq_answer', '')
    vacancy_id = dialog_manager.dialog_data.get('vacancy_id')
    file_data = dialog_manager.dialog_data.get("new_faq_file")

    vacancy_data = Vacancy.get_by_id(vacancy_id=vacancy_id)

    # DynamicMedia
    if file_data:
        file_type = file_data["type"]
        file_id = file_data["file_id"]
        if file_type == "photo":
            media = MediaAttachment(ContentType.PHOTO, file_id=MediaId(file_id))
        elif file_type == "video":
            media = MediaAttachment(ContentType.VIDEO, file_id=MediaId(file_id))
        else:
            media = MediaAttachment(ContentType.DOCUMENT, file_id=MediaId(file_id))
    else:
        media = None

    file_info = f"📎 Файл загружен: {file_data['type']}" if file_data else "📎 Файл не добавлен"

    dialog_manager.dialog_data['media'] = media

    bot_logger.warning(f"dialog_data: {dialog_manager.dialog_data}")
    bot_logger.warning(F"media: {media}")

    return {
        "new_faq_question": new_faq_question,
        "new_faq_answer": new_faq_answer,
        "vacancy_title": vacancy_data.title,
        "media": media,
        "file_info": file_info
    }


async def new_faq_question_getter(dialog_manager: DialogManager, **_kwargs):
    new_faq_question = dialog_manager.dialog_data['new_faq_question']

    return {
        'new_faq_question': new_faq_question,
    }
