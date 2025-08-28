from aiogram_dialog import DialogManager

from src.database.dataclasses.vacancy_faq_dataclass import VacancyFAQ


async def vacancy_faq_answer_getter(dialog_manager: DialogManager, **_kwargs):
    vacancy_faq_id = int(dialog_manager.dialog_data['vacancy_faq_id'])
    faq = VacancyFAQ.get_by_id(vacancy_faq_id)

    return {
        "faq_found": bool(faq),
        "question": faq.question if faq else None,
        "answer": faq.answer if faq else None
    }

