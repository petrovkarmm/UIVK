from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram_dialog import DialogManager

from app.dialogs.uivk_dialog.uivk_dialog_states import UivkDialogStatesGroup
from aiogram import Router

start_router = Router()


@start_router.message(Command('start'))
async def start_dialog_command(message: Message, state: FSMContext, dialog_manager: DialogManager):
    await dialog_manager.start(
        UivkDialogStatesGroup.uivk_start_menu
    )
