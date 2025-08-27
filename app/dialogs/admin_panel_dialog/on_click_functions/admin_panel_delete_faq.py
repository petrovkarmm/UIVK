from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager

from app.database.dataclasses.vacancy_faq_dataclass import VacancyFAQ
from app.dialogs.admin_panel_dialog.admin_dialog_states import AdminPanelStatesGroup


async def on_click_delete_faq(
        callback: CallbackQuery,
        widget: Any,
        dialog_manager: DialogManager,
):
    vacancy_faq_id = dialog_manager.dialog_data['vacancy_faq_id']

    VacancyFAQ.delete_by_id(vacancy_faq_id)

    await dialog_manager.switch_to(
        AdminPanelStatesGroup.admin_panel_vacancy_and_questions
    )