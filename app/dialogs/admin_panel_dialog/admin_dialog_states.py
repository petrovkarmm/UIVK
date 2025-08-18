from aiogram.fsm.state import StatesGroup, State


class AdminPanelStatesGroup(StatesGroup):
    admin_panel_menu = State()

    admin_panel_vacancy_and_questions = State()
    admin_panel_vacancy_deleting = State()

    admin_panel_vacancy_faq_answer = State()
    admin_panel_vacancy_faq_creating = State()
