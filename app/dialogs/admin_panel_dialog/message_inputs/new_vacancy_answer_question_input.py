from aiogram.types import ContentType, Message
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog import (
    Dialog,
    Window,
    DialogManager,
)

from app.dialogs.admin_panel_dialog.admin_dialog_states import AdminPanelStatesGroup


async def new_faq_answer_input(
        message: Message,
        _message_input,  # не используешь — подчёркни, чтобы линтер не ругался
        dialog_manager: DialogManager,
):
    new_faq_answer = (message.text or "").strip()
    if not new_faq_answer:
        await message.answer('🤔 Похоже, вы отправили что-то не то...')
        return

    dialog_manager.dialog_data['new_faq_answer'] = new_faq_answer

    await dialog_manager.switch_to(
        AdminPanelStatesGroup.admin_panel_vacancy_faq_accept_creating
    )
