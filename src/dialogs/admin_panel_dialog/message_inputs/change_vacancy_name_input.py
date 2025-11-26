from aiogram.types import ContentType, Message
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog import (
    Dialog,
    Window,
    DialogManager,
)

from src.database.dataclasses.vacancy import Vacancy
from src.dialogs.admin_panel_dialog.admin_dialog_states import AdminPanelStatesGroup


async def change_vacancy_name_input(
        message: Message,
        _message_input,
        dialog_manager: DialogManager,
):
    vacancy_id = dialog_manager.dialog_data['vacancy_id']

    Vacancy.update_title(
        vacancy_id=vacancy_id,
        new_title=message.text
    )

    await dialog_manager.switch_to(
        AdminPanelStatesGroup.admin_panel_vacancy_and_questions
    )
