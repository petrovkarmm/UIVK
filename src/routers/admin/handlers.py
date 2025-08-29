import os

from aiogram import Router, F
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram_dialog import DialogManager

from src.database.dataclasses.admin import Admin
from src.database.dataclasses.chat_group import ChatGroup
from src.database.dataclasses.topic import Topic
from src.dialogs.admin_panel_dialog.admin_dialog_states import AdminPanelStatesGroup
from src.logs.logger import bot_logger
from src.filters.admin_filters import IsAdminFilter, IsSuperAdminFilter

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


@admin_panel.message(Command("set_group"), IsSuperAdminFilter())
async def set_group(message: Message, state: FSMContext, dialog_manager: DialogManager, command: CommandObject):
    try:
        group_id = int(command.args.strip())
    except (ValueError, AttributeError):
        await message.answer("❌ Использование: /set_group <group_id>")
        return

    cg = ChatGroup.create(group_id=group_id)
    await message.answer(
        f"✅ Группа установлена:\n"
        f"- Group ID: {cg.group_id}"
    )


@admin_panel.message(Command("get_group"), IsSuperAdminFilter())
async def get_group(message: Message, state: FSMContext, dialog_manager: DialogManager):
    cg = ChatGroup.get()
    if not cg:
        await message.answer("⚠️ Группа ещё не настроена.")
        return

    await message.answer(f"ℹ️ Текущие настройки группы:\n"
                         f"- Group ID: {cg.group_id}")


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


@admin_panel.message(Command("help"), IsAdminFilter())
async def admin_help_commands_handler(message: Message):
    await message.answer(
        text=f'Общие команды:\n'
             f'/id - получение ID пользователя (может использовать любой)\n'
             f'/list_admins - получение списка администраторов\n\n'
             f'Команды супер-администратора\n'
             f'/add telegram_id - добавление администратора\n'
             f'/remove telegram_id - удаление администратора\n'
             f'/get_group - получение ID группы администраторов (где происходит переписка с пользователями)\n'
             f'/set_group group_id - выставление новой группы\n\n'
             f'Переписку с пользователями в топиках могут производить только администраторы.'
    )


@admin_panel.message(Command("list_admins"), IsAdminFilter())
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


@admin_panel.message(
    IsAdminFilter(),
    F.chat.type.in_({"group", "supergroup"}),
    F.text
)
async def admin_message_handler(message: Message):
    if message.from_user.is_bot:
        return

    thread_id = getattr(message, "message_thread_id", None)

    # если это General — скипаем
    if thread_id is None:
        return

    # находим топик в базе
    topic = Topic.get_by_topic_id(thread_id)
    if not topic:
        await message.answer("⚠️ Не найден пользователь для этого топика.")
        return

    # отправляем сообщение пользователю
    try:
        await message.bot.send_message(
            chat_id=topic.user_id,
            text=message.text
        )
        await message.answer("✨ Сообщение успешно отправлено!")
    except Exception as e:
        await message.answer(f"❌ Ошибка при отправке пользователю: {e}")
