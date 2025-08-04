from aiogram_dialog import DialogManager


async def vacancy_faq_answer_getter(dialog_manager: DialogManager, **_kwargs):
    vacancy_faq_id = dialog_manager.dialog_data['vacancy_faq_id']
    return {
        'test': vacancy_faq_id
    }
