from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager

from src.dialogs.admin_panel_dialog.admin_dialog_states import AdminPanelStatesGroup
from src.logs.logger import bot_logger


async def on_click_go_to_admin_panel(
        callback: CallbackQuery,
        widget: Any,
        dialog_manager: DialogManager,
):
    try:
        await dialog_manager.reset_stack()
    except Exception as e:
        bot_logger.warning(e)
    finally:
        await dialog_manager.start(
            AdminPanelStatesGroup.admin_panel_menu
        )
