from app.database.dataclasses.vacancy_dataclass import Vacancy


async def new_vacancy_name_input(
        message: Message,
        message_input: MessageInput,
        dialog_manager: DialogManager,
):
    new_vacancy_name = message.text
    if new_vacancy_name:
        vacancy = Vacancy.create_new(vacancy_name=new_vacancy_name)
        new_vacancy_id = vacancy['id']
        dialog_manager.dialog_data['vacancy_id'] = new_vacancy_id
        await dialog_manager.switch_to(
            AdminPanelStatesGroup.admin_panel_vacancy_and_questions
        )
    else:
        await message.answer(
            text='🤔 Похоже, вы отправили что-то не то...'
        )
