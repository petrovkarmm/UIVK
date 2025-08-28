from src.database.dataclasses.admin_dataclass import Admin
from src.settings import super_admins


async def admin_status_checker(user_id: int) -> bool:
    return (str(user_id) in super_admins) or Admin.exists(user_id)


async def super_admin_status_checker(user_id: int) -> bool:
    return str(user_id) in super_admins