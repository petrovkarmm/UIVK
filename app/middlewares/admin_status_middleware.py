import os
from typing import Callable, Dict, Any, Awaitable, Union

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager

from app.database.dataclasses.admin_dataclass import Admin
from app.dialogs.uivk_dialog.uivk_dialog_states import UivkDialogStatesGroup


class KickDeletedAdminFromAdminPanel(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[
                [Union[Message, CallbackQuery], Dict[str, Any]],
                Awaitable[Any],
            ],
            event: Union[Message, CallbackQuery],
            data: Dict[str, Any],
    ) -> Any:
        user_id = event.from_user.id

        super_admins = [
            i.strip()
            for i in os.getenv("MAIN_ADMIN_TELEGRAM_IDS", "").split(",")
            if i.strip()
        ]

        dialog_manager: DialogManager = data.get("dialog_manager")

        # Если это супер-админ или админ в базе - продолжаем
        if (str(user_id) in super_admins) or Admin.exists(user_id):
            return await handler(event, data)

        # Если пользователь потерял права админа
        await event.answer("❌ У вас больше нет прав администратора.")

        if dialog_manager is not None:
            try:
                await dialog_manager.reset_stack()
            except Exception as e:
                # Логирование ошибки сброса стека
                print(f"Ошибка reset_stack: {e}")
            finally:
                # Переводим в обычный диалог
                await dialog_manager.start(
                    UivkDialogStatesGroup.uivk_start_menu
                )
        return None
