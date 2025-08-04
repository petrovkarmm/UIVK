from aiogram import Router

from app.dialogs.admin_panel_dialog.admin_panel_dialog import admin_panel_dialog

admin_panel_dialog_router = Router()

admin_panel_dialog_router.include_router(admin_panel_dialog)
