from aiogram import Router

from app.dialogs.uivk_dialog.uivk_dialog import uivk_dialog

uivk_dialog_router = Router()

uivk_dialog_router.include_router(uivk_dialog)
