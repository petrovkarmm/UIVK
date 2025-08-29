from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from src.dialogs.admin_panel_dialog.admin_dialog_states import AdminPanelStatesGroup


async def on_click_next_file(c: CallbackQuery, button: Button, dialog_manager: DialogManager):
    new_faq_file = dialog_manager.dialog_data.get('new_faq_file')

    # Если файла нет — чистим dialog_data
    if not new_faq_file:
        dialog_manager.dialog_data.pop('new_faq_file', None)

    # Переходим на итоговое окно
    await dialog_manager.switch_to(AdminPanelStatesGroup.admin_panel_vacancy_faq_accept_creating)

async def on_click_clear_file(c, button, dialog_manager: DialogManager):
    dialog_manager.dialog_data.pop("new_faq_file", None)
    await c.message.answer("♻️ Файл удалён.")

