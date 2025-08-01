from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager

from app.dialogs.uivk_dialog.uivk_dialog_states import UivkDialogStatesGroup


async def on_click_vacancy_faq_selected(
        callback: CallbackQuery,
        widget: Any,
        dialog_manager: DialogManager,
        vacancy_faq_id: int,
):
    dialog_manager.dialog_data['vacancy_faq_id'] = vacancy_faq_id

    await callback.answer(
        text=str(vacancy_faq_id)
    )
