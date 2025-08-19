from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager

from app.database.dataclasses.vacancy_dataclass import Vacancy
from app.dialogs.admin_panel_dialog.admin_dialog_states import AdminPanelStatesGroup


async def on_click_delete_vacancy(
        callback: CallbackQuery,
        widget: Any,
        dialog_manager: DialogManager,
):
    vacancy_id = dialog_manager.dialog_data['vacancy_id']
    Vacancy.delete_by_id(vacancy_id)
    await dialog_manager.switch_to(
        AdminPanelStatesGroup.admin_panel_menu
    )
