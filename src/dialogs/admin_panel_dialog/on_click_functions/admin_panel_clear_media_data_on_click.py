from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager

from src.dialogs.admin_panel_dialog.admin_dialog_states import AdminPanelStatesGroup


async def on_click_clear_all_media_data_on_click(
        callback: CallbackQuery,
        widget: Any,
        dialog_manager: DialogManager,
):
    dialog_manager.dialog_data.pop("new_faq_file", None)
    dialog_manager.dialog_data.pop("media", None)
    await dialog_manager.switch_to(AdminPanelStatesGroup.admin_panel_vacancy_faq_question_creating)