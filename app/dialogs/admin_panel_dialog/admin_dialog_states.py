from aiogram.fsm.state import StatesGroup, State


class AdminPanelStatesGroup(StatesGroup):
    admin_panel_menu = State()
    admin_panel_vacancy = State()
    admin_panel_faq = State()
