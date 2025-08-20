from aiogram import F
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import ScrollingGroup, Column, Select, Button, Row, SwitchTo
from aiogram_dialog.widgets.text import Format

from app.database.dataclasses.vacancy_dataclass import VACANCY_KEY
from app.database.dataclasses.vacancy_faq_dataclass import VACANCY_FAQ_KEY
from app.dialogs.admin_panel_dialog.admin_dialog_states import AdminPanelStatesGroup
from app.dialogs.admin_panel_dialog.getters.admin_vacancy_getter import all_admin_vacancy_getter, \
    admin_current_vacancy_getter
from app.dialogs.admin_panel_dialog.on_click_functions.admin_panel_delete_vacancy_on_click import \
    on_click_delete_vacancy
from app.dialogs.admin_panel_dialog.on_click_functions.admin_panel_faq_on_click import \
    on_click_vacancy_faq_admin_panel_selected
from app.dialogs.admin_panel_dialog.on_click_functions.admin_panel_on_click import go_to_bot_from_admin_panel
from app.dialogs.admin_panel_dialog.on_click_functions.admin_panel_vacancy_on_click import \
    on_click_vacancy_admin_panel_selected
from app.dialogs.uivk_dialog.getters.vacancy_faq_answer_getter import vacancy_faq_answer_getter
from app.dialogs.uivk_dialog.getters.vacancy_faq_getter import vacancy_faq_id_getter, vacancy_faq_getter
from app.dialogs.uivk_dialog.getters.vacancy_getter import vacancy_id_getter
from app.dialogs.uivk_dialog.on_click_functions.vacancy_faq_on_click import on_click_vacancy_faq_selected
from app.dialogs.uivk_dialog.on_click_functions.vacancy_on_click import on_click_vacancy_selected

admin_start_panel_window = Window(
    Format(
        text='Добро пожаловать в админ панель бота УИВК. Выберите вакансию для редактирования:',
        when=F['vacancy_data_flag']
    ),
    ScrollingGroup(
        Column(
            Select(
                text=Format("{item.vacancy_name}"),
                id="adm_vacancy_selected",
                items=VACANCY_KEY,
                item_id_getter=vacancy_id_getter,
                on_click=on_click_vacancy_admin_panel_selected,
            ),
        ),
        width=2,
        height=5,
        id="adm_scroll_vacancy",
        hide_on_single_page=True,
        when=F['vacancy_data_flag']
    ),
    Format(
        text='На текущий момент вакансии отсутствуют. Нажмите Создать, чтобы добавить новую вакансию.',
        when=~F['vacancy_data_flag']
    ),
    SwitchTo(
        id='to_new_vacancy', text=Format('Создать вакансию'), state=AdminPanelStatesGroup.admin_panel_vacancy_creating
    ),
    Button(
        id='back_to_bot', text=Format(
            text='Назад в бота'
        ),
        on_click=go_to_bot_from_admin_panel
    ),
    getter=all_admin_vacancy_getter,
    state=AdminPanelStatesGroup.admin_panel_menu
)

admin_vacancy_faq_answer_window = Window(
    Format(
        text='Выберите интересующий вас вопрос по вакансии:',
        when=F['vacancy_faq_data_flag']
    ),
    Format(
        text='FAQ на данную должность отсутствует.', # TODO передавать имя вакансии и отображать текстом тут.
        when=~F['vacancy_faq_data_flag']
    ),
    ScrollingGroup(
        Column(
            Select(
                text=Format("{item.question}"),
                id="faq_selected",
                items=VACANCY_FAQ_KEY,
                item_id_getter=vacancy_faq_id_getter,
                on_click=on_click_vacancy_faq_admin_panel_selected,
            ),
        ),
        width=2,
        height=5,
        id="scroll_faq",
        hide_on_single_page=True,
        when=F['vacancy_faq_data_flag']
    ),
    SwitchTo(
        id='to_creating',
        text=Format('Добавить FAQ'),
        state=AdminPanelStatesGroup.admin_panel_vacancy_faq_creating
    ),
    SwitchTo(
        id='to_deleting',
        text=Format('Удалить вакансию'),
        state=AdminPanelStatesGroup.admin_panel_vacancy_deleting
    ),
    Button(
        id='update_faq', text=Format('Обновить'), on_click=None,
        when=~F['vacancy_faq_data_flag']
    ),
    Row(
        SwitchTo(
            id='back_to_start',
            text=Format('Назад в меню'),
            state=AdminPanelStatesGroup.admin_panel_menu
        ),
        Button(
            id='back_to_bot', text=Format(
                text='Назад в бота'),
            on_click=go_to_bot_from_admin_panel
        )
    ),
    getter=vacancy_faq_getter,
    state=AdminPanelStatesGroup.admin_panel_vacancy_and_questions,
    parse_mode="HTML"
)

admin_vacancy_deleting_window = Window(
    Format(
        text='Данные: создание: {vacancy_created} редактирование {vacancy_updated}\n'
             'Вы уверенны, что хотите удалить вакансию "{vacancy_name}". Статус - {vacancy_status}?'
    ),
    Button(
        id='delete_vac', text=Format('Удалить'), on_click=on_click_delete_vacancy
    ),
    Row(
        SwitchTo(
            id='back_to_start',
            text=Format('Назад в меню'),
            state=AdminPanelStatesGroup.admin_panel_menu
        ),
        Button(
            id='back_to_bot', text=Format(
                text='Назад в бота'),
            on_click=go_to_bot_from_admin_panel
        )
    ),
    getter=admin_current_vacancy_getter,
    state=AdminPanelStatesGroup.admin_panel_vacancy_deleting
)

admin_vacancy_creating_window = Window(
    Format(
        text='Введите новое название вакансии'
    ),
    MessageInput(
        new_vacancy_name_input
    ),
    Row(
        SwitchTo(
            id='back_to_start',
            text=Format('Назад в меню'),
            state=AdminPanelStatesGroup.admin_panel_menu
        ),
        Button(
            id='back_to_bot', text=Format(
                text='Назад в бота'),
            on_click=go_to_bot_from_admin_panel
        )
    ),
    state=AdminPanelStatesGroup.admin_panel_vacancy_creating
)

admin_panel_dialog = Dialog(
    admin_start_panel_window,
    admin_vacancy_faq_answer_window,
    admin_vacancy_deleting_window
)
