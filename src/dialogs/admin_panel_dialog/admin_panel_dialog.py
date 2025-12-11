from aiogram import F
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import ScrollingGroup, Column, Select, Button, SwitchTo, Row
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Format, Multi

from src.database.dataclasses.vacancy import VACANCY_KEY
from src.database.dataclasses.vacancy_faq import VACANCY_FAQ_KEY
from src.dialogs.admin_panel_dialog.admin_dialog_states import AdminPanelStatesGroup
from src.dialogs.admin_panel_dialog.getters.admin_answer_and_question_getter import new_faq_answer_and_question_getter, \
    new_faq_question_getter
from src.dialogs.admin_panel_dialog.getters.admin_vacancy_faq_file_getter import new_faq_file_getter
from src.dialogs.admin_panel_dialog.getters.admin_vacancy_faq_getter import admin_vacancy_faq_getter
from src.dialogs.admin_panel_dialog.getters.admin_vacancy_getter import all_admin_vacancy_getter, \
    admin_current_vacancy_getter
from src.dialogs.admin_panel_dialog.message_inputs.change_vacancy_faq_answer_input import \
    change_vacancy_faq_answer_input
from src.dialogs.admin_panel_dialog.message_inputs.change_vacancy_faq_question_input import \
    change_vacancy_faq_question_input
from src.dialogs.admin_panel_dialog.message_inputs.change_vacancy_name_input import change_vacancy_name_input
from src.dialogs.admin_panel_dialog.message_inputs.new_faq_answer_question_input import new_faq_answer_input
from src.dialogs.admin_panel_dialog.message_inputs.new_faq_file_input import new_faq_file_input
from src.dialogs.admin_panel_dialog.message_inputs.new_faq_question_input import new_faq_question_input
from src.dialogs.admin_panel_dialog.message_inputs.new_vacancy_name_input import new_vacancy_title_input
from src.dialogs.admin_panel_dialog.on_click_functions.admin_panel_clear_media_data_on_click import \
    on_click_clear_all_media_data_on_click
from src.dialogs.admin_panel_dialog.on_click_functions.admin_panel_file_adding_on_click import on_click_clear_file, \
    on_click_next_file
from src.dialogs.admin_panel_dialog.on_click_functions.admin_panel_change_hidden_status_on_click import \
    on_click_change_vacancy_hidden_status
from src.dialogs.admin_panel_dialog.on_click_functions.admin_panel_create_new_faq_on_click import \
    on_click_create_new_faq
from src.dialogs.admin_panel_dialog.on_click_functions.admin_panel_delete_faq import on_click_delete_faq
from src.dialogs.admin_panel_dialog.on_click_functions.admin_panel_delete_vacancy_on_click import \
    on_click_delete_vacancy
from src.dialogs.admin_panel_dialog.on_click_functions.admin_panel_faq_on_click import \
    on_click_vacancy_faq_admin_panel_selected
from src.dialogs.admin_panel_dialog.on_click_functions.admin_panel_on_click import go_to_bot_from_admin_panel
from src.dialogs.admin_panel_dialog.on_click_functions.admin_panel_vacancy_on_click import \
    on_click_vacancy_admin_panel_selected
from src.dialogs.uivk_dialog.getters.vacancy_faq_answer_getter import vacancy_faq_answer_getter
from src.dialogs.uivk_dialog.getters.vacancy_faq_getter import vacancy_faq_id_getter
from src.dialogs.uivk_dialog.getters.vacancy_getter import vacancy_id_getter

admin_start_panel_window = Window(
    Format(
        text='👋 Добро пожаловать в <b>админ-панель</b> бота <b>УИВК</b>!\n\n'
             '📂 Выберите вакансию для редактирования:',
        when=F['vacancy_data_flag']
    ),
    ScrollingGroup(
        Column(
            Select(
                text=Format("💼 {item.title}"),
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
        text='⚠️ На данный момент вакансии <b>отсутствуют</b>.\n\n'
             '➕ Нажмите <b>Создать вакансию</b>, чтобы добавить новую.',
        when=~F['vacancy_data_flag']
    ),
    SwitchTo(
        id='to_new_vacancy',
        text=Format('➕ Создать вакансию'),
        state=AdminPanelStatesGroup.admin_panel_vacancy_creating
    ),
    Button(
        id='back_to_bot',
        text=Format('⬅️ Назад в бота'),
        on_click=go_to_bot_from_admin_panel
    ),
    getter=all_admin_vacancy_getter,
    state=AdminPanelStatesGroup.admin_panel_menu,
    parse_mode="HTML"
)

admin_vacancy_faq_answer_window = Window(
    Format(
        text='🗂️ <b>Данные вакансии {vacancy_title}:</b>\n\n'
             '📌 Статус: <b>{vacancy_status}</b>\n'
             '📅 Создана: <b>{vacancy_created}</b>\n'
             '✏️ Изменена: <b>{vacancy_updated}</b>\n\n'
             '❓ Выберите интересующий вас вопрос по вакансии:',
        when=F['vacancy_faq_data_flag']
    ),
    Format(
        text='🗂️ <b>Данные вакансии {vacancy_title}:</b>\n\n'
             '📌 Статус: <b>{vacancy_status}</b>\n'
             '📅 Создана: <b>{vacancy_created}</b>\n'
             '✏️ Изменена: <b>{vacancy_updated}</b>\n\n'
             '⚠️ Для вакансии <b>{vacancy_title}</b> пока нет FAQ.\n\n'
             '➕ Нажмите кнопку <b>Добавить FAQ</b> ниже, чтобы создать первый вопрос.',
        when=~F['vacancy_faq_data_flag']
    ),
    ScrollingGroup(
        Column(
            Select(
                text=Format("❓ {item.question}"),
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
    Button(
        id='change_hidden',
        text=Format('🔄 Поменять статус'),
        on_click=on_click_change_vacancy_hidden_status),
    SwitchTo(
        id='change_name',
        text=Format('🔄 Поменять название'),
        state=AdminPanelStatesGroup.admin_panel_vacancy_name_change),
    Button(
        id='to_creating',
        text=Format('➕ Добавить FAQ'),
        on_click=on_click_clear_all_media_data_on_click
    ),
    SwitchTo(
        id='to_deleting',
        text=Format('🗑️ Удалить вакансию'),
        state=AdminPanelStatesGroup.admin_panel_vacancy_deleting
    ),
    SwitchTo(
        id='back_to_start',
        text=Format('⬅️ Назад в меню'),
        state=AdminPanelStatesGroup.admin_panel_menu
    ),
    getter=admin_vacancy_faq_getter,
    state=AdminPanelStatesGroup.admin_panel_vacancy_and_questions,
    parse_mode="HTML"
)

admin_vacancy_name_change = Window(
    Format(
        text="✍️ <b>Введите новое название вакансии:</b>"
    ),
    MessageInput(
        change_vacancy_name_input
    ),
    SwitchTo(
        id="to_admin_vacancy",
        text=Format("⬅️ Назад"),
        state=AdminPanelStatesGroup.admin_panel_vacancy_and_questions
    ),
    SwitchTo(
        id='back_to_start',
        text=Format('⬅️ Назад в меню'),
        state=AdminPanelStatesGroup.admin_panel_menu
    ),
    state=AdminPanelStatesGroup.admin_panel_vacancy_name_change,
    parse_mode="HTML"
)

admin_vacancy_faq_deleting = Window(
    Format(
        "⚠️ Вы уверены, что хотите удалить данный FAQ?\n\n"
        "<b>❓ Вопрос:</b>\n{question}\n\n"
        "<b>💬 Ответ:</b>\n{answer}",
        when=F["faq_found"]
    ),
    DynamicMedia("media", when=F["media"]),
    Format(
        "😅 Ой, что-то пошло не так — FAQ не найден.",
        when=~F["faq_found"]
    ),
    Button(
        id='delete_faq',
        text=Format('🗑️ Да, удаляем!'),
        on_click=on_click_delete_faq
    ),
    SwitchTo(
        id="to_admin_faq",
        text=Format("⬅️ Назад"),
        state=AdminPanelStatesGroup.admin_panel_vacancy_faq_answer
    ),
    SwitchTo(
        id='back_to_start',
        text=Format('🏠 Назад в меню'),
        state=AdminPanelStatesGroup.admin_panel_menu
    ),
    getter=vacancy_faq_answer_getter,
    state=AdminPanelStatesGroup.admin_panel_vacancy_faq_deleting,
    parse_mode="HTML"
)

admin_vacancy_faq_answer = Window(
    Format(
        "<b>❓ Вопрос:</b>\n{question}\n\n"
        "<b>💬 Ответ:</b>\n{answer}",
        when=F["faq_found"]
    ),
    DynamicMedia("media", when=F["media"]),
    Format(
        "😅 Ой, что-то пошло не так — FAQ не найден.",
        when=~F["faq_found"]
    ),
    SwitchTo(
        id='to_delete_faq',
        text=Format('🗑️ Удалить FAQ'),
        state=AdminPanelStatesGroup.admin_panel_vacancy_faq_deleting
    ),
    SwitchTo(
        id="change_question",
        text=Format('🔄 Поменять вопрос'),
        state=AdminPanelStatesGroup.admin_panel_vacancy_faq_changing_question
    ),
    SwitchTo(
        id="change_question",
        text=Format('🔄 Поменять ответ'),
        state=AdminPanelStatesGroup.admin_panel_vacancy_faq_changing_answer
    ),
    SwitchTo(
        id="to_admin_faq",
        text=Format("⬅️ Назад"),
        state=AdminPanelStatesGroup.admin_panel_vacancy_and_questions
    ),
    SwitchTo(
        id='back_to_start',
        text=Format('🏠 Назад в меню'),
        state=AdminPanelStatesGroup.admin_panel_menu
    ),
    getter=vacancy_faq_answer_getter,
    state=AdminPanelStatesGroup.admin_panel_vacancy_faq_answer,
    parse_mode="HTML"
)

admin_vacancy_deleting_window = Window(
    Format(
        text='🗂️ <b>Данные вакансии {vacancy_title}:</b>\n\n'
             '📌 Статус: <b>{vacancy_status}</b>\n'
             '📅 Создана: <b>{vacancy_created}</b>\n'
             '✏️ Изменена: <b>{vacancy_updated}</b>\n\n'
             '⚠️ Вы уверены, что хотите удалить вакансию\n'
             '«<b>{vacancy_title}</b>»?\n'
    ),
    Button(
        id='delete_vac',
        text=Format('🗑️ Удалить вакансию'),
        on_click=on_click_delete_vacancy
    ),
    SwitchTo(
        id='back',
        text=Format('⬅️ Назад'),
        state=AdminPanelStatesGroup.admin_panel_vacancy_and_questions
    ),
    SwitchTo(
        id='back_to_start',
        text=Format('🏠 Назад в меню'),
        state=AdminPanelStatesGroup.admin_panel_menu
    ),
    getter=admin_current_vacancy_getter,
    state=AdminPanelStatesGroup.admin_panel_vacancy_deleting,
    parse_mode="HTML"
)

admin_vacancy_creating_window = Window(
    Format(
        text='✍️ <b>Введите новое название вакансии:</b>'
    ),
    MessageInput(
        new_vacancy_title_input
    ),
    SwitchTo(
        id='back_to_start',
        text=Format('🏠 Назад в меню'),
        state=AdminPanelStatesGroup.admin_panel_menu
    ),
    state=AdminPanelStatesGroup.admin_panel_vacancy_creating,
    parse_mode="HTML"
)

admin_vacancy_faq_question_change = Window(
    Format(
        text="✍️ <b>Введите новый вопрос:</b>"
    ),
    MessageInput(
        change_vacancy_faq_question_input
    ),
    SwitchTo(
        id="to_admin_faq",
        text=Format("⬅️ Назад"),
        state=AdminPanelStatesGroup.admin_panel_vacancy_faq_answer
    ),
    SwitchTo(
        id='back_to_start',
        text=Format('⬅️ Назад в меню'),
        state=AdminPanelStatesGroup.admin_panel_menu
    ),
    state=AdminPanelStatesGroup.admin_panel_vacancy_faq_changing_question,
    parse_mode="HTML"
)

admin_vacancy_faq_answer_change = Window(
    Format(
        text="✍️ <b>Введите новый ответ:</b>"
    ),
    MessageInput(
        change_vacancy_faq_answer_input
    ),
    SwitchTo(
        id="to_admin_faq",
        text=Format("⬅️ Назад"),
        state=AdminPanelStatesGroup.admin_panel_vacancy_faq_answer
    ),
    SwitchTo(
        id='back_to_start',
        text=Format('⬅️ Назад в меню'),
        state=AdminPanelStatesGroup.admin_panel_menu
    ),
    state=AdminPanelStatesGroup.admin_panel_vacancy_faq_changing_answer,
    parse_mode="HTML"
)

admin_vacancy_faq_question_creating_window = Window(
    Format(
        text='❓ <b>Введите новый вопрос для FAQ:</b>'
    ),
    MessageInput(
        new_faq_question_input
    ),
    SwitchTo(
        id='back_to_vacancy',
        text=Format('⬅️ Назад'),
        state=AdminPanelStatesGroup.admin_panel_vacancy_and_questions
    ),
    SwitchTo(
        id='back_to_start',
        text=Format('🏠 Назад в меню'),
        state=AdminPanelStatesGroup.admin_panel_menu
    ),
    state=AdminPanelStatesGroup.admin_panel_vacancy_faq_question_creating,
    parse_mode="HTML"
)

admin_vacancy_faq_answer_creating_window = Window(
    Format(
        text='❓ <b>Вопрос:</b> {new_faq_question}\n\n'
             '💬 <b>Введите ответ на вопрос:</b>'
    ),
    MessageInput(
        new_faq_answer_input
    ),
    SwitchTo(
        id='back_to_question',
        text=Format('⬅️ Назад'),
        state=AdminPanelStatesGroup.admin_panel_vacancy_faq_question_creating
    ),
    SwitchTo(
        id='back_to_start',
        text=Format('🏠 Назад в меню'),
        state=AdminPanelStatesGroup.admin_panel_menu
    ),
    getter=new_faq_question_getter,
    state=AdminPanelStatesGroup.admin_panel_vacancy_faq_answer_creating,
    parse_mode="HTML"
)

admin_vacancy_faq_accept_creating_window = Window(
    Format(
        text=(
            "✅ <b>Проверьте вводимые данные:</b>\n\n"
            "💼 <b>Вакансия:</b> {vacancy_title}\n\n"
            "❓ <b>Вопрос:</b> {new_faq_question}\n"
            "💬 <b>Ответ:</b> {new_faq_answer}\n"
            "{file_info}"
        )
    ),
    DynamicMedia("media", when=F["media"]),  # Показываем только если media есть
    Button(
        id='create_faq',
        text=Format('➕ Создать FAQ'),
        on_click=on_click_create_new_faq
    ),
    SwitchTo(
        id='back_to_question',
        text=Format('⬅️ Назад'),
        state=AdminPanelStatesGroup.admin_panel_vacancy_faq_files_creating
    ),
    SwitchTo(
        id='back_to_start',
        text=Format('🏠 Назад в меню'),
        state=AdminPanelStatesGroup.admin_panel_menu
    ),
    getter=new_faq_answer_and_question_getter,
    state=AdminPanelStatesGroup.admin_panel_vacancy_faq_accept_creating,
    parse_mode="HTML"
)

admin_panel_vacancy_faq_file_creating_window = Window(
    Format(
        text=(
            "📎 <b>Прикрепление файла</b>\n\n"
            "Можно загрузить 1 файл любого формата (фото, видео, документ).\n"
            "Количество загруженных файлов: {file_count}\n\n"
            "Нажмите <b>Далее</b>, когда закончите загрузку файла."
        )
    ),
    MessageInput(new_faq_file_input),
    Button(
        id="next_file",
        text=Format("⏭ Далее"),
        on_click=on_click_next_file
    ),
    Button(
        id="clear_file",
        text=Format("♻️ Очистить"),
        on_click=on_click_clear_file,
        when=F["has_file"]
    ),
    SwitchTo(
        id="back_to_answer",
        text=Format("⬅️ Назад"),
        state=AdminPanelStatesGroup.admin_panel_vacancy_faq_answer_creating
    ),
    SwitchTo(
        id='back_to_start',
        text=Format('🏠 Назад в меню'),
        state=AdminPanelStatesGroup.admin_panel_menu
    ),
    getter=new_faq_file_getter,
    state=AdminPanelStatesGroup.admin_panel_vacancy_faq_files_creating,
    parse_mode="HTML"
)

admin_panel_dialog = Dialog(
    admin_start_panel_window,
    admin_vacancy_faq_answer_window,

    admin_vacancy_faq_answer,
    admin_vacancy_faq_deleting,

    admin_vacancy_deleting_window,
    admin_vacancy_creating_window,

    admin_vacancy_faq_question_creating_window,
    admin_vacancy_faq_answer_creating_window,
    admin_panel_vacancy_faq_file_creating_window,

    admin_vacancy_faq_accept_creating_window,

    admin_vacancy_name_change,

    admin_vacancy_faq_question_change,
    admin_vacancy_faq_answer_change

)
