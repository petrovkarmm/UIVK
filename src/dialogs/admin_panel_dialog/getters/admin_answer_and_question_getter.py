from pprint import pprint
from typing import Dict, Any

from aiogram.enums import ContentType
from aiogram.types import InputMediaPhoto, InputMediaVideo, InputMediaDocument
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import MediaAttachment, MediaId

from src.database.dataclasses.vacancy import Vacancy


async def new_faq_answer_and_question_getter(dialog_manager: DialogManager, **_kwargs):
    new_faq_question = dialog_manager.dialog_data.get('new_faq_question', '')
    new_faq_answer = dialog_manager.dialog_data.get('new_faq_answer', '')
    vacancy_id = dialog_manager.dialog_data.get('vacancy_id')
    file_data = dialog_manager.dialog_data.get("new_faq_file")

    vacancy_data = Vacancy.get_by_id(vacancy_id=vacancy_id)

    # DynamicMedia
    if file_data:
        ftype = file_data["type"]
        fid = file_data["file_id"]
        if ftype == "photo":
            media = MediaAttachment(ContentType.PHOTO, file_id=MediaId(fid))
        elif ftype == "video":
            media = MediaAttachment(ContentType.VIDEO, file_id=MediaId(fid))
        else:
            media = MediaAttachment(ContentType.DOCUMENT, file_id=MediaId(fid))
    else:
        media = None

    files_info = f"📎 Файл загружен: {file_data['type']}" if file_data else "📎 Файл не добавлен"

    return {
        "new_faq_question": new_faq_question,
        "new_faq_answer": new_faq_answer,
        "vacancy_title": vacancy_data.title,
        "media": media,
        "files_info": files_info
    }


async def new_faq_question_getter(dialog_manager: DialogManager, **_kwargs):
    new_faq_question = dialog_manager.dialog_data['new_faq_question']

    return {
        'new_faq_question': new_faq_question,
    }
