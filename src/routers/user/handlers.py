from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager, ShowMode

from src.database.dataclasses.chat_group import ChatGroup
from src.dialogs.uivk_dialog.uivk_dialog_states import UivkDialogStatesGroup
from aiogram import Router, F

from src.logs.logger import bot_logger

user_panel = Router()


@user_panel.message(Command('start'), F.chat.type == "private")
async def start_dialog_command(message: Message, state: FSMContext, dialog_manager: DialogManager):
    chat_group = ChatGroup.get()
    chat_group_id = chat_group.group_id

    if chat_group:
        user_id = message.from_user.id
        first_name = message.from_user.first_name or "Имя отсутствует"
        last_name = message.from_user.last_name or "Фамилия отсутствует"
        username = f"@{message.from_user.username}" if message.from_user.username else "Username отсутствует"

        await message.bot.send_message(
            chat_id=chat_group_id,
            text=(
                f"👻 Новый пользователь бота! \n\n"
                f"{first_name} {last_name} ({username}, ID: {user_id})"
            )
        )
    else:
        bot_logger.warning("⚠️ Админская группа не настроена.")

    await dialog_manager.start(
        UivkDialogStatesGroup.uivk_start_menu
    )


@user_panel.message(F.text, F.chat.type == "private")
async def start_dialog_text(message: Message, state: FSMContext, dialog_manager: DialogManager):
    await dialog_manager.start(
        UivkDialogStatesGroup.uivk_start_menu
    )
