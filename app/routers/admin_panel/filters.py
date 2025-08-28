from aiogram.filters import BaseFilter
from aiogram.types import Message
import os

from app.database.dataclasses.admin_dataclass import Admin


class IsAdminFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        user_id = message.from_user.id

        # Получаем super admin id из .env
        main_admin_id = os.getenv("MAIN_ADMIN_TELEGRAM_ID")

        if main_admin_id and str(user_id) == str(main_admin_id):
            return True

        # Проверяем, есть ли в БД
        return Admin.exists(user_id)
