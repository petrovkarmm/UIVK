from aiogram_dialog import DialogManager

from test_data import test_vacancy_data


async def vacancy_faq_getter(dialog_manager: DialogManager, **_kwargs):
    vacancy_id = dialog_manager.dialog_data['vacancy_id']

    print(vacancy_id),

    vacancy_faq = test_vacancy_data[vacancy_id]
    print(vacancy_faq)

    # TODO добавить нормальную базу данных.


def current_vacancy_getter(vacancy_id: list):
    for vacancy in test_vacancy_data:
        if vacancy_id == vacancy['id']:
            return
