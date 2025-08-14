from aiogram import F
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import ScrollingGroup, Column, Select, Button
from aiogram_dialog.widgets.text import Format

from app.database.dataclasses.vacancy_dataclass import VACANCY_KEY
from app.dialogs.admin_panel_dialog.admin_dialog_states import AdminPanelStatesGroup
from app.dialogs.admin_panel_dialog.getters.admin_vacancy_getter import all_admin_vacancy_getter
from app.dialogs.admin_panel_dialog.on_click_functions.admin_panel_on_click import go_to_bot_from_admin_panel
from app.dialogs.uivk_dialog.getters.vacancy_getter import vacancy_id_getter
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
                on_click=on_click_vacancy_selected,
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
    Button(
        id='back_to_bot', text=Format(
            text='Назад в бота'),
        on_click=go_to_bot_from_admin_panel
    ),
    getter=all_admin_vacancy_getter,
    state=AdminPanelStatesGroup.admin_panel_menu
)

admin_panel_dialog = Dialog(
    admin_start_panel_window
)
