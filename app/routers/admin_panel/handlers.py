from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram_dialog import DialogManager

from app.dialogs.admin_panel_dialog.admin_dialog_states import AdminPanelStatesGroup
from app.logs.logger import bot_logger

admin_panel = Router()


@admin_panel.message(F.text == 'admin_test')
async def start_admin_panel_dialog(message: Message, state: FSMContext, dialog_manager: DialogManager):
    # TODO протестить поведение 2-х групп.
    try:
        await dialog_manager.close_manager()
    except Exception as e:
        bot_logger.warning(e)
    finally:
        await dialog_manager.start(
            AdminPanelStatesGroup.admin_panel_menu
        )
