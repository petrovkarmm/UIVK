from pprint import pprint

from aiogram.enums import ContentType
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import MediaAttachment, MediaId

from src.database.dataclasses.vacancy_faq import VacancyFAQ


async def vacancy_faq_answer_getter(dialog_manager: DialogManager, **_kwargs):
    vacancy_faq_id = int(dialog_manager.dialog_data['vacancy_faq_id'])
    faq = VacancyFAQ.get_by_id(vacancy_faq_id)

    if faq.media:
        file_type = faq.media["file_type"]
        file_id = faq.media["file_id"]
        file_id = "asdasdasdqewqwe23123"
        if file_type == "photo":
            media = MediaAttachment(ContentType.PHOTO, file_id=MediaId(file_id))
        elif file_type == "video":
            media = MediaAttachment(ContentType.VIDEO, file_id=MediaId(file_id))
        else:
            media = MediaAttachment(ContentType.DOCUMENT, file_id=MediaId(file_id))
    else:
        media = None

    print(media)

    return {
        "faq_found": bool(faq),
        "question": faq.question if faq else None,
        "answer": faq.answer if faq else None,
        "media": media,
    }
