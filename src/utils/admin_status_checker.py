from src.database.dataclasses.admin import Admin
from src.settings import super_admins

#TODO переместить в статик методы класса Admin

def admin_status_checker(user_id: int) -> bool:
    return (str(user_id) in super_admins) or Admin.exists(user_id)


def super_admin_status_checker(user_id: int) -> bool:
    return str(user_id) in super_admins
