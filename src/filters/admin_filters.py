from dotenv import load_dotenv, find_dotenv

from aiogram.filters import BaseFilter
from aiogram.types import Message
from src.utils.admin_status_checker import admin_status_checker, super_admin_status_checker


class IsAdminFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        user_id = message.from_user.id

        admin_status = await admin_status_checker(user_id)

        if admin_status:
            return True
        else:
            await message.answer("❌ У вас нет прав администратора.")
            return False


class IsSuperAdminFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        user_id = message.from_user.id

        super_admin_status = await super_admin_status_checker(user_id)

        if super_admin_status:
            return True
        else:
            await message.answer("❌ У вас нет прав супер администратора.")
            return False