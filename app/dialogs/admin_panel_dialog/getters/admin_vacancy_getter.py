from aiogram_dialog import DialogManager

from app.database.dataclasses.vacancy_dataclass import Vacancy, VACANCY_KEY


async def all_admin_vacancy_getter(dialog_manager: DialogManager, **_kwargs):
    vacancies = Vacancy.get_all(include_hidden=True)
    vacancy_data_flag = bool(vacancies)

    for vacancy in vacancies:
        vacancy.vacancy_name = Vacancy.formatted_hidden_vacancy(
            vacancy.vacancy_name,
            vacancy.hidden_status
        )

    return {
        VACANCY_KEY: vacancies,
        "vacancy_data_flag": vacancy_data_flag
    }


async def admin_current_vacancy_getter(dialog_manager: DialogManager, **_kwargs):
    vacancy_id = dialog_manager.dialog_data['vacancy_id']
    vacancy_data = Vacancy.get_by_id(vacancy_id)

    vacancy_name = vacancy_data.vacancy_name
    vacancy_hidden_status = vacancy_data.hidden_status
    vacancy_created = vacancy_data.created
    vacancy_updated = vacancy_data.updated

    print(vacancy_updated)
    print(vacancy_created)

    if vacancy_hidden_status:
        vacancy_status = "скрыта"
    else:
        vacancy_status = "открыта"

    return {
        'vacancy_name': vacancy_name,
        'vacancy_status': vacancy_status,
        'vacancy_created': vacancy_created,
        'vacancy_updated': vacancy_updated
    }
