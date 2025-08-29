from pprint import pprint

from aiogram_dialog import DialogManager

from src.database.dataclasses.vacancy_dataclass import Vacancy, VACANCY_KEY
from src.utils.admin_status_checker import admin_status_checker


async def all_unhidden_vacancy_getter(dialog_manager: DialogManager, **_kwargs):
    vacancies = Vacancy.get_all(include_hidden=False)
    vacancy_data_flag = bool(vacancies)

    user = dialog_manager.middleware_data.get('event_from_user').id
    admin_status = admin_status_checker(user)

    for vacancy in vacancies:
        vacancy.title = Vacancy.format_title(vacancy.title)

    return {
        VACANCY_KEY: vacancies,
        "vacancy_data_flag": vacancy_data_flag,
        "admin_status": admin_status,
    }


def vacancy_id_getter(vacancy: Vacancy) -> int:
    return vacancy.id
