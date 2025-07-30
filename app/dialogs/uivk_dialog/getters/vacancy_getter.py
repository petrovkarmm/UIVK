from pprint import pprint

from aiogram_dialog import DialogManager

from app.dialogs.uivk_dialog.dataclasses.vacancy_dataclass import Vacancy, VACANCY_KEY
from test_data import test_vacancy_data


async def all_vacancy_getter(dialog_manager: DialogManager, **_kwargs):
    # TODO Добавить логику форматирования названия, чтобы избежать
    # @staticmethod
    # def formatted_feedback_text(feedback_text: str):
    #     return f'{feedback_text[:15]}...'

    if test_vacancy_data:
        vacancy_data_flag = True
    else:
        vacancy_data_flag = False

    return {
        VACANCY_KEY: [
            Vacancy(
                id=vacancy['id'], vacancy_name=vacancy['vacancy_name']
            )
            for vacancy in test_vacancy_data
        ],
        'vacancy_data_flag': vacancy_data_flag
    }


def vacancy_id_getter(vacancy: Vacancy) -> int:
    return vacancy.id
