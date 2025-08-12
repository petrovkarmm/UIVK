from pprint import pprint

from aiogram_dialog import DialogManager

from app.dialogs.uivk_dialog.dataclasses.vacancy_dataclass import Vacancy, VACANCY_KEY
from test_data import test_vacancy_data


async def all_vacancy_getter(dialog_manager: DialogManager, **_kwargs):
    vacancies = Vacancy.get_all()
    vacancy_data_flag = bool(vacancies)

    # Форматируем названия
    for vacancy in vacancies:
        vacancy.vacancy_name = Vacancy.format_name(vacancy.vacancy_name)

    return {
        VACANCY_KEY: vacancies,
        "vacancy_data_flag": vacancy_data_flag
    }


def vacancy_id_getter(vacancy: Vacancy) -> int:
    return vacancy.id
