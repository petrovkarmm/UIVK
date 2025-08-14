from aiogram_dialog import DialogManager

from app.database.dataclasses.vacancy_dataclass import Vacancy, VACANCY_KEY


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
