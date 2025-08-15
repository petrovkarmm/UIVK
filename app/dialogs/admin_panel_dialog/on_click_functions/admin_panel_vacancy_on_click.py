from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager

from app.dialogs.admin_panel_dialog.admin_dialog_states import AdminPanelStatesGroup


async def on_click_vacancy_admin_panel_selected(
        callback: CallbackQuery,
        widget: Any,
        dialog_manager: DialogManager,
        vacancy_id: int,
):
    dialog_manager.dialog_data['vacancy_id'] = vacancy_id

    await dialog_manager.switch_to(
        AdminPanelStatesGroup.admin_panel_vacancy_and_questions
    )
