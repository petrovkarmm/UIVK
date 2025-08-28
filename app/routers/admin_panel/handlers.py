import os

from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram_dialog import DialogManager

from app.database.dataclasses.admin_dataclass import Admin
from app.dialogs.admin_panel_dialog.admin_dialog_states import AdminPanelStatesGroup
from app.logs.logger import bot_logger
from app.filters.admin_filters import IsAdminFilter, IsSuperAdminFilter

admin_panel = Router()


@admin_panel.message(Command("add"), IsSuperAdminFilter())
async def add_new_admin(message: Message, state: FSMContext, dialog_manager: DialogManager, command: CommandObject):
    try:
        new_admin_telegram_id = int(command.args.strip())
    except (ValueError, AttributeError):
        await message.answer("Укажите корректный Telegram ID: /add <id>")
        return

    if Admin.add(new_admin_telegram_id):
        await message.answer(f"✅ Админ с ID {new_admin_telegram_id} успешно добавлен.")
    else:
        await message.answer(f"⚠️ Админ с ID {new_admin_telegram_id} уже есть в базе.")


@admin_panel.message(Command("remove"), IsSuperAdminFilter())
async def delete_admin(message: Message, state: FSMContext, dialog_manager: DialogManager, command: CommandObject):
    try:
        admin_telegram_id = int(command.args.strip())
    except (ValueError, AttributeError):
        await message.answer("Укажите корректный Telegram ID: /remove <id>")
        return

    if Admin.delete(admin_telegram_id):
        await message.answer(f"🗑 Админ с ID {admin_telegram_id} удалён.")
    else:
        await message.answer(f"❌ Админ с ID {admin_telegram_id} не найден в базе.")


@admin_panel.message(Command("list_admins"), IsSuperAdminFilter())
async def list_admins_handler(message: Message, state: FSMContext, dialog_manager: DialogManager,
                              command: CommandObject):
    # Обычные админы из базы (set, чтобы быстро убирать дубли)
    db_admins = {str(admin.telegram_id) for admin in Admin.all()}

    super_admins = {i.strip() for i in os.getenv("MAIN_ADMIN_TELEGRAM_IDS", "").split(",") if i.strip()}

    # Исключаем дубли — супер-админов не дублируем в "обычных"
    db_admins -= super_admins

    def format_block(title: str, ids: set[str], emoji: str) -> str:
        if ids:
            return f"{emoji} <b>{title}</b>:\n" + "\n".join(f"• <code>{i}</code>" for i in sorted(ids)) + "\n\n"
        return f"{emoji} <b>{title}</b>: (нет)\n\n"

    response = (
            "👑 <b>Список администраторов</b>\n\n"
            + format_block("Супер-админы", super_admins, "✨")
            + format_block("Админы", db_admins, "🛡")
    )

    await message.answer(response.strip(), parse_mode="HTML")


@admin_panel.message(Command('admin'), IsAdminFilter())
async def start_admin_panel_dialog(message: Message, state: FSMContext, dialog_manager: DialogManager,
                                   command: CommandObject):
    try:
        await dialog_manager.reset_stack()
    except Exception as e:
        bot_logger.warning(e)
    finally:
        await dialog_manager.start(
            AdminPanelStatesGroup.admin_panel_menu
        )


@admin_panel.message(Command("help"), IsAdminFilter())
async def help_admin_handler(message: Message, state: FSMContext, command: CommandObject):
    help_text = (
        "<b>Команды администратора:</b>\n"
        "▫️ <code>/admin</code> — открыть админ-панель (доступно всем администраторам)\n"
        "▫️ <code>/id</code> — узнать свой Telegram ID (можно использовать для добавления в админы)\n\n"

        "<b>Команды супер-администратора:</b>\n"
        "▫️ <code>/add 123456789</code> — добавить администратора (укажите Telegram ID)\n"
        "▫️ <code>/remove 123456789</code> — удалить администратора (по Telegram ID)\n"
        "▫️ <code>/list_admins</code> — список всех администраторов\n"
    )

    await message.answer(help_text, parse_mode="HTML")

