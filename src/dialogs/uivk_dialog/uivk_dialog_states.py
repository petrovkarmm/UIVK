from aiogram.fsm.state import StatesGroup, State


class UivkDialogStatesGroup(StatesGroup):
    uivk_start_menu = State()
    uivk_vacancy_and_questions = State()
    uivk_vacancy_faq_answer = State()
    uivk_dialog_with_admins = State()