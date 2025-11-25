from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager

from src.dialogs.uivk_dialog.uivk_dialog_states import UivkDialogStatesGroup


async def on_click_go_to_chat_with_manager(
        callback: CallbackQuery,
        widget: Any,
        dialog_manager: DialogManager,
):
    dialog_manager.dialog_data['vacancy_id'] = None
    await dialog_manager.switch_to(
        UivkDialogStatesGroup.uivk_dialog_with_admins
    )
