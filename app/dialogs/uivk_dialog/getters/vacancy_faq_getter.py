from aiogram_dialog import DialogManager

from app.dialogs.uivk_dialog.dataclasses.vacancy_faq_dataclass import VACANCY_FAQ_KEY, VacancyFAQ
from test_data import test_vacancy_data


async def vacancy_faq_getter(dialog_manager: DialogManager, **_kwargs):
    vacancy_id = dialog_manager.dialog_data['vacancy_id']

    print(vacancy_id),

    all_vacancy_faq = current_vacancy_getter(vacancy_id=vacancy_id)

    print(all_vacancy_faq)

    # TODO Добавить логику форматирования названия, чтобы избежать
    # @staticmethod
    # def formatted_feedback_text(feedback_text: str):
    #     return f'{feedback_text[:15]}...'

    if all_vacancy_faq:
        vacancy_faq_data_flag = True
    else:
        vacancy_faq_data_flag = False

    return {
        VACANCY_FAQ_KEY: [
            VacancyFAQ(
                id=vacancy_faq['id'], question=vacancy_faq['question']
            )
            for vacancy_faq in all_vacancy_faq
        ],
        'vacancy_faq_data_flag': vacancy_faq_data_flag
    }


def vacancy_faq_id_getter(vacancy_faq: VacancyFAQ) -> int:
    return vacancy_faq.id


def current_vacancy_getter(vacancy_id: list):
    for vacancy in test_vacancy_data:
        print(vacancy['id'])
        if vacancy_id == vacancy['id']:
            return vacancy['faq']
