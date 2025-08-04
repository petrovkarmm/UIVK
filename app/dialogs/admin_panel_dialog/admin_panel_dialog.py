from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Format

from app.dialogs.admin_panel_dialog.admin_dialog_states import AdminPanelStatesGroup

admin_start_panel_window = Window(
    Format(
        text='Test admin panel window'
    ),
    state=AdminPanelStatesGroup.admin_panel_menu
)

admin_panel_dialog = Dialog(
    admin_start_panel_window
)
