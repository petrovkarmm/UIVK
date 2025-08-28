from aiogram_dialog import DialogManager

from src.database.dataclasses.vacancy_dataclass import Vacancy
from src.database.dataclasses.vacancy_faq_dataclass import VacancyFAQ, VACANCY_FAQ_KEY


async def admin_vacancy_faq_getter(dialog_manager: DialogManager, **_kwargs):
    vacancy_id = dialog_manager.dialog_data['vacancy_id']
    vacancy_data = Vacancy.get_by_id(vacancy_id)

    vacancy_title = vacancy_data.title
    vacancy_hidden_status = vacancy_data.hidden
    vacancy_created = vacancy_data.created
    vacancy_updated = vacancy_data.updated

    faqs = VacancyFAQ.get_by_vacancy_id(vacancy_id=vacancy_id)
    vacancy_faq_data_flag = bool(faqs)

    for faq in faqs:
        faq.question = VacancyFAQ.format_question(faq.question)

    if vacancy_hidden_status:
        vacancy_status = "скрыта"
    else:
        vacancy_status = "открыта"

    return {
        VACANCY_FAQ_KEY: faqs,
        'vacancy_title': vacancy_title,
        'vacancy_status': vacancy_status,
        'vacancy_created': vacancy_created,
        'vacancy_updated': vacancy_updated,
        'vacancy_faq_data_flag': vacancy_faq_data_flag
    }
