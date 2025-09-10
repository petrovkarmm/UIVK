from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager

from src.dialogs.uivk_dialog.uivk_dialog_states import UivkDialogStatesGroup
from aiogram import Router, F

start_router = Router()


@start_router.message(Command('start'), F.chat.type == "private")
async def start_dialog_command(message: Message, state: FSMContext, dialog_manager: DialogManager):
    await dialog_manager.start(
        UivkDialogStatesGroup.uivk_start_menu
    )


@start_router.message(F.text, F.chat.type == "private")
async def start_dialog_text(message: Message, state: FSMContext, dialog_manager: DialogManager):
    await dialog_manager.start(
        UivkDialogStatesGroup.uivk_start_menu
    )


@start_router.callback_query(F.data == "reply_to_admin")
async def on_reply_to_admin(
        callback: CallbackQuery,
        dialog_manager: DialogManager
):
    await callback.answer()

    await dialog_manager.start(
        state=UivkDialogStatesGroup.uivk_dialog_with_admins,
    )
