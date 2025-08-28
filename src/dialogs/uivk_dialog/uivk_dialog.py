from aiogram import F
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import ScrollingGroup, Column, Select, Button, SwitchTo, Row
from aiogram_dialog.widgets.text import Format

from src.database.dataclasses.vacancy_dataclass import VACANCY_KEY
from src.database.dataclasses.vacancy_faq_dataclass import VACANCY_FAQ_KEY
from src.dialogs.uivk_dialog.getters.vacancy_faq_answer_getter import vacancy_faq_answer_getter
from src.dialogs.uivk_dialog.getters.vacancy_faq_getter import vacancy_faq_getter, vacancy_faq_id_getter
from src.dialogs.uivk_dialog.getters.vacancy_getter import vacancy_id_getter, all_unhidden_vacancy_getter
from src.dialogs.uivk_dialog.on_click_functions.vacancy_faq_on_click import on_click_vacancy_faq_selected
from src.dialogs.uivk_dialog.on_click_functions.vacancy_on_click import on_click_vacancy_selected
from src.dialogs.uivk_dialog.uivk_dialog_states import UivkDialogStatesGroup

uivk_start_window = Window(
    Format(
        text='👋 Добро пожаловать в телеграм-бот проекта <b>УИВК</b>!\n\n'
             '➡️ Чтобы перейти на следующий этап, выберите позицию вашего отклика:',
        when=F['vacancy_data_flag']
    ),
    ScrollingGroup(
        Column(
            Select(
                text=Format("💼 {item.title}"),
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
        text='⚠️ На данный момент открытые вакансии отсутствуют!',
        when=~F['vacancy_data_flag']
    ),
    Button(
        id='update_vacancy',
        text=Format('🔄 Обновить'),
        on_click=None,
        when=~F['vacancy_data_flag']
    ),
    getter=all_unhidden_vacancy_getter,
    state=UivkDialogStatesGroup.uivk_start_menu,
    parse_mode="HTML"
)


uivk_vacancy_faq_window = Window(
    Format(
        text='❓ Выберите интересующий вас вопрос по вакансии <b>{vacancy_title}</b>:',
        when=F['vacancy_faq_data_flag']
    ),
    Format(
        text='⚠️ FAQ на должность <b>{vacancy_title}</b> отсутствует.',
        when=~F['vacancy_faq_data_flag']
    ),
    ScrollingGroup(
        Column(
            Select(
                text=Format("❓ {item.question}"),
                id="faq_selected",
                items=VACANCY_FAQ_KEY,
                item_id_getter=vacancy_faq_id_getter,
                on_click=on_click_vacancy_faq_selected,
            ),
        ),
        width=2,
        height=5,
        id="scroll_faq",
        hide_on_single_page=True,
        when=F['vacancy_faq_data_flag']
    ),
    Button(
        id='update_faq',
        text=Format('🔄 Обновить'),
        on_click=None,
        when=~F['vacancy_faq_data_flag']
    ),
    SwitchTo(
        id='to_vacancy',
        text=Format('⬅️ Назад'),
        state=UivkDialogStatesGroup.uivk_start_menu
    ),
    getter=vacancy_faq_getter,
    state=UivkDialogStatesGroup.uivk_vacancy_and_questions,
    parse_mode="HTML"
)


uivk_vacancy_faq_answer_window = Window(
    Format(
        text='❓ <b>Вопрос:</b>\n{question}\n\n'
             '💬 <b>Ответ:</b>\n{answer}',
        when=F["faq_found"]
    ),
    Format(
        text='😅 Ой, что-то пошло не так — FAQ не найден.',
        when=~F["faq_found"]
    ),
    SwitchTo(
        id="to_faq",
        text=Format('⬅️ Назад'),
        state=UivkDialogStatesGroup.uivk_vacancy_and_questions
    ),
    SwitchTo(
        id="to_vacancy",
        text=Format('🏠 В меню вакансий'),
        state=UivkDialogStatesGroup.uivk_start_menu
    ),
    getter=vacancy_faq_answer_getter,
    state=UivkDialogStatesGroup.uivk_vacancy_faq_answer,
    parse_mode="HTML"
)


uivk_dialog = Dialog(
    uivk_start_window,
    uivk_vacancy_faq_window,
    uivk_vacancy_faq_answer_window
)
