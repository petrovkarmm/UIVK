from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager

from src.database.dataclasses.vacancy import Vacancy


async def on_click_change_vacancy_hidden_status(
        callback: CallbackQuery,
        widget: Any,
        dialog_manager: DialogManager,
):
    vacancy_id = dialog_manager.dialog_data['vacancy_id']
    Vacancy.toggle_hidden(vacancy_id)
