from aiogram.fsm.state import StatesGroup, State


class UivkDialogStatesGroup(StatesGroup):
    uivk_start_menu = State()
    uivk_vacancy_faq = State()
    uivk_vacancy_faq_answer = State()
