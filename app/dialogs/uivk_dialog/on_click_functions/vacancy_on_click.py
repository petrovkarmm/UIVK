from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager

from app.dialogs.uivk_dialog.uivk_dialog_states import UivkDialogStatesGroup


async def on_click_vacancy_selected(
        callback: CallbackQuery,
        widget: Any,
        dialog_manager: DialogManager,
        vacancy_id: int,
):
    dialog_manager.dialog_data['vacancy_id'] = vacancy_id

    await dialog_manager.switch_to(
        UivkDialogStatesGroup.uivk_vacancy_and_questions
    )
