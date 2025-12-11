from aiogram.types import ContentType, Message
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog import (
    Dialog,
    Window,
    DialogManager,
)
from src.database.dataclasses.vacancy_faq import VacancyFAQ
from src.dialogs.admin_panel_dialog.admin_dialog_states import AdminPanelStatesGroup


async def change_vacancy_faq_answer_input(
        message: Message,
        _message_input,
        dialog_manager: DialogManager,
):
    vacancy_faq_id = dialog_manager.dialog_data['vacancy_faq_id']

    VacancyFAQ.update_answer(
        faq_id=vacancy_faq_id,
        new_answer=message.text
    )

    await dialog_manager.switch_to(
        AdminPanelStatesGroup.admin_panel_vacancy_faq_answer
    )
