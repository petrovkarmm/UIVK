from aiogram_dialog import DialogManager

from src.database.dataclasses.vacancy import Vacancy


async def new_faq_answer_and_question_getter(dialog_manager: DialogManager, **_kwargs):
    new_faq_question = dialog_manager.dialog_data['new_faq_question']
    new_faq_answer = dialog_manager.dialog_data['new_faq_answer']
    vacancy_id = dialog_manager.dialog_data['vacancy_id']

    vacancy_data = Vacancy.get_by_id(vacancy_id=vacancy_id)

    return {
        'new_faq_question': new_faq_question,
        'new_faq_answer': new_faq_answer,
        'vacancy_title': vacancy_data.title
    }


async def new_faq_question_getter(dialog_manager: DialogManager, **_kwargs):
    new_faq_question = dialog_manager.dialog_data['new_faq_question']

    return {
        'new_faq_question': new_faq_question,
    }
