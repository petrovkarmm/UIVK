import os

from dotenv import load_dotenv, find_dotenv

from aiogram.filters import BaseFilter
from aiogram.types import Message

from app.database.dataclasses.admin_dataclass import Admin

load_dotenv(find_dotenv())


class IsAdminFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        user_id = message.from_user.id

        super_admins = [i.strip() for i in os.getenv("MAIN_ADMIN_TELEGRAM_IDS", "").split(",") if i.strip()]

        # Проверка супер-админа
        if str(user_id) in super_admins:
            return True

        # Проверка обычного админа
        if Admin.exists(user_id):
            return True

        # Пользователь не админ — отправляем сообщение
        await message.answer("❌ У вас нет прав администратора.")
        return False


class IsSuperAdminFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:

        user_id = message.from_user.id

        super_admins = {i.strip() for i in os.getenv("MAIN_ADMIN_TELEGRAM_IDS", "").split(",") if i.strip()}

        # Проверка супер-админа
        if str(user_id) in super_admins:
            return True

        # Пользователь не админ — отправляем сообщение
        await message.answer("❌ У вас нет прав администратора.")
        return False
