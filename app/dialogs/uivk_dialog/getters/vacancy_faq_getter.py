from aiogram_dialog import DialogManager

from app.database.dataclasses.vacancy_faq_dataclass import VACANCY_FAQ_KEY, VacancyFAQ
from test_data import test_vacancy_data


async def vacancy_faq_getter(dialog_manager: DialogManager, **_kwargs):
    vacancy_id = int(dialog_manager.dialog_data['vacancy_id'])

    faqs = VacancyFAQ.get_by_vacancy_id(vacancy_id)
    vacancy_faq_data_flag = bool(faqs)

    # Форматируем вопросы
    for faq in faqs:
        faq.question = VacancyFAQ.format_question(faq.question)

    return {
        VACANCY_FAQ_KEY: faqs,
        'vacancy_faq_data_flag': vacancy_faq_data_flag
    }


def vacancy_faq_id_getter(vacancy_faq: VacancyFAQ) -> int:
    return vacancy_faq.id


def current_vacancy_getter(vacancy_id: int):
    for vacancy in test_vacancy_data:
        print(vacancy_id, vacancy['id'])
        print(vacancy['faq'])
        if vacancy_id == vacancy['id']:
            print(vacancy['faq'])
            return vacancy['faq']

    return []  # <= добавь это!
