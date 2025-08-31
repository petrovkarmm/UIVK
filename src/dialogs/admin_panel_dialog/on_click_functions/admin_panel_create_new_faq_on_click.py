from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import MediaAttachment

from src.database.dataclasses.vacancy_faq import VacancyFAQ
from src.dialogs.admin_panel_dialog.admin_dialog_states import AdminPanelStatesGroup


async def on_click_create_new_faq(
        callback: CallbackQuery,
        widget: Any,
        dialog_manager: DialogManager,
):
    vacancy_id = dialog_manager.dialog_data['vacancy_id']
    new_faq_question = dialog_manager.dialog_data['new_faq_question']
    new_faq_answer = dialog_manager.dialog_data['new_faq_answer']
    file_data = dialog_manager.dialog_data.get("new_faq_file")

    if file_data:
        file_type = file_data["type"]
        file_id = file_data["file_id"]

        media_data = {
            'file_type': file_type,
            'file_id': file_id,
        }
    else:
        media_data = None

    VacancyFAQ.create_new(
        vacancy_id=vacancy_id,
        question=new_faq_question,
        answer=new_faq_answer,
        media=media_data
    )

    await dialog_manager.switch_to(
        AdminPanelStatesGroup.admin_panel_vacancy_and_questions
    )
