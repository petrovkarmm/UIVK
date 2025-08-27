from aiogram_dialog import DialogManager

from app.database.dataclasses.vacancy_dataclass import Vacancy, VACANCY_KEY


async def all_admin_vacancy_getter(dialog_manager: DialogManager, **_kwargs):
    vacancies = Vacancy.get_all(include_hidden=True)
    vacancy_data_flag = bool(vacancies)

    for vacancy in vacancies:
        vacancy.title = Vacancy.formatted_title_hidden_vacancy(
            vacancy.title,
            vacancy.hidden
        )

    return {
        VACANCY_KEY: vacancies,
        "vacancy_data_flag": vacancy_data_flag
    }


async def admin_current_vacancy_getter(dialog_manager: DialogManager, **_kwargs):
    vacancy_id = dialog_manager.dialog_data['vacancy_id']
    vacancy_data = Vacancy.get_by_id(vacancy_id)

    vacancy_title = vacancy_data.title
    vacancy_hidden_status = vacancy_data.hidden
    vacancy_created = vacancy_data.created
    vacancy_updated = vacancy_data.updated

    if vacancy_hidden_status:
        vacancy_status = "скрыта"
    else:
        vacancy_status = "открыта"

    return {
        'vacancy_title': vacancy_title,
        'vacancy_status': vacancy_status,
        'vacancy_created': vacancy_created,
        'vacancy_updated': vacancy_updated
    }
