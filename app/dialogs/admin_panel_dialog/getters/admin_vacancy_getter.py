from aiogram_dialog import DialogManager

from app.database.dataclasses.vacancy_dataclass import Vacancy, VACANCY_KEY


async def all_admin_vacancy_getter(dialog_manager: DialogManager, **_kwargs):
    vacancies = Vacancy.get_all()
    vacancy_data_flag = bool(vacancies)

    # Форматируем названия
    for vacancy in vacancies:
        vacancy.vacancy_name = Vacancy.formatted_hidden_vacancy(vacancy.vacancy_name, vacancy.hidden)

    return {
        VACANCY_KEY: vacancies,
        "vacancy_data_flag": vacancy_data_flag
    }
