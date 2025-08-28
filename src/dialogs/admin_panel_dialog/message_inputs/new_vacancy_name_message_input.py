from src.database.dataclasses.vacancy_dataclass import Vacancy
from aiogram.types import ContentType, Message
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog import (
    Dialog,
    Window,
    DialogManager,
)

from src.dialogs.admin_panel_dialog.admin_dialog_states import AdminPanelStatesGroup


async def new_vacancy_title_input(
        message: Message,
        _message_input,  # не используешь — подчёркни, чтобы линтер не ругался
        dialog_manager: DialogManager,
):
    new_vacancy_title = (message.text or "").strip()
    if not new_vacancy_title:
        await message.answer('🤔 Похоже, вы отправили что-то не то...')
        return

    vacancy = Vacancy.create_new(title=new_vacancy_title)  # возвращает dataclass
    dialog_manager.dialog_data['vacancy_id'] = vacancy.id  # <-- вот так, через точку
    await dialog_manager.switch_to(
        AdminPanelStatesGroup.admin_panel_vacancy_and_questions
    )