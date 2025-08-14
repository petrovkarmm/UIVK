from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager

from app.dialogs.uivk_dialog.uivk_dialog_states import UivkDialogStatesGroup
from app.logs.logger import bot_logger


async def go_to_bot_from_admin_panel(
        callback: CallbackQuery,
        widget: Any,
        dialog_manager: DialogManager,
):
    try:
        await dialog_manager.done()
    except Exception as e:
        bot_logger.warning(e)
    finally:
        await dialog_manager.start(
            UivkDialogStatesGroup.uivk_start_menu
        )
