from aiogram import F
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import ScrollingGroup, Column, Select, Button
from aiogram_dialog.widgets.text import Format

from app.dialogs.uivk_dialog.dataclasses.vacancy_dataclass import VACANCY_KEY
from app.dialogs.uivk_dialog.getters.vacancy_faq_getter import vacancy_faq_getter
from app.dialogs.uivk_dialog.getters.vacancy_getter import vacancy_id_getter, all_vacancy_getter
from app.dialogs.uivk_dialog.on_click_functions.vacancy_on_click import on_click_vacancy_selected
from app.dialogs.uivk_dialog.uivk_dialog_states import UivkDialogStatesGroup

uivk_start_window = Window(
    Format(
        text='Добро пожаловать в телеграмм бота проекта УИВК!\n'
             'Чтобы перейти на следующий этап, выберите позицию вашего отклика:',
        when=F['vacancy_data_flag']

    ),
    ScrollingGroup(
        Column(
            Select(
                text=Format("{item.vacancy_name}"),
                id="vacancy_selected",
                items=VACANCY_KEY,
                item_id_getter=vacancy_id_getter,
                on_click=on_click_vacancy_selected,
            ),
        ),
        width=2,
        height=5,
        id="scroll_vacancy",
        hide_on_single_page=True,
        when=F['vacancy_data_flag']
    ),
    Format(
        text='На текущий момент открытые вакансии отсутствуют!',
        when=~F['vacancy_data_flag']
    ),
    Button(
        id='update_vacancy', text=Format('Обновить'), on_click=None,
        when=~F['vacancy_data_flag']
    ),
    getter=all_vacancy_getter,
    state=UivkDialogStatesGroup.uivk_start_menu
)

uivk_vacancy_faq_window = Window(
    Format(
        text='Выберите интересующий вас вопрос по вакансии:'
    ),
    getter=vacancy_faq_getter,
    state=UivkDialogStatesGroup.uivk_vacancy_faq
)

uivk_dialog = Dialog(
    uivk_start_window,
    uivk_vacancy_faq_window
)
