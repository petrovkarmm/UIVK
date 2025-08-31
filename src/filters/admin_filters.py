from dotenv import load_dotenv, find_dotenv

from aiogram.filters import BaseFilter
from aiogram.types import Message

from src.database.dataclasses.admin import Admin


class IsAdminFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if message.from_user.is_bot:
            return True

        user_id = message.from_user.id
        if Admin.admin_status_checker(user_id):
            return True

        await message.answer("❌ У вас нет прав администратора.")
        return False


class IsSuperAdminFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if message.from_user.is_bot:
            return False

        user_id = message.from_user.id
        if Admin.super_admin_status_checker(user_id):
            return True

        await message.answer("❌ У вас нет прав супер администратора.")
        return False
