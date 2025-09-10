from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager, ShowMode

from src.dialogs.uivk_dialog.uivk_dialog_states import UivkDialogStatesGroup
from aiogram import Router, F

user_panel = Router()


@user_panel.message(Command('start'), F.chat.type == "private")
async def start_dialog_command(message: Message, state: FSMContext, dialog_manager: DialogManager):
    await dialog_manager.start(
        UivkDialogStatesGroup.uivk_start_menu
    )


@user_panel.message(F.text, F.chat.type == "private")
async def start_dialog_text(message: Message, state: FSMContext, dialog_manager: DialogManager):
    await dialog_manager.start(
        UivkDialogStatesGroup.uivk_start_menu
    )
