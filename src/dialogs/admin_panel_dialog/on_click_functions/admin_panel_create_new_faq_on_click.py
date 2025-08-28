from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager

from src.database.dataclasses.vacancy_faq_dataclass import VacancyFAQ
from src.dialogs.admin_panel_dialog.admin_dialog_states import AdminPanelStatesGroup


async def on_click_create_new_faq(
        callback: CallbackQuery,
        widget: Any,
        dialog_manager: DialogManager,
):
    vacancy_id = dialog_manager.dialog_data['vacancy_id']
    new_faq_question = dialog_manager.dialog_data['new_faq_question']
    new_faq_answer = dialog_manager.dialog_data['new_faq_answer']

    VacancyFAQ.create_new(
        vacancy_id=vacancy_id,
        question=new_faq_question,
        answer=new_faq_answer
    )

    await dialog_manager.switch_to(
        AdminPanelStatesGroup.admin_panel_vacancy_and_questions
    )
