from aiogram_dialog import DialogManager

from src.database.dataclasses.vacancy_dataclass import Vacancy, VACANCY_KEY


async def all_unhidden_vacancy_getter(dialog_manager: DialogManager, **_kwargs):
    vacancies = Vacancy.get_all(include_hidden=False)
    vacancy_data_flag = bool(vacancies)

    for vacancy in vacancies:
        vacancy.title = Vacancy.format_title(vacancy.title)

    return {
        VACANCY_KEY: vacancies,
        "vacancy_data_flag": vacancy_data_flag
    }


def vacancy_id_getter(vacancy: Vacancy) -> int:
    return vacancy.id
