from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message
from aiogram_dialog import (
    DialogManager,
)

from src.database.dataclasses.chat_group import ChatGroup
from src.database.dataclasses.topic import Topic
from src.database.dataclasses.vacancy import Vacancy
from src.logs.logger import bot_logger

exception_message = "❗ Не удалось доставить сообщение HR-менеджерам. Пожалуйста, сообщите об ошибке сотруднику через HH."


async def user_question_input(
        message: Message,
        _message_input,
        dialog_manager: DialogManager,
):
    vacancy_id = dialog_manager.dialog_data['vacancy_id']
    if vacancy_id:
        vacancy_data = Vacancy.get_by_id(vacancy_id=vacancy_id)
        vacancy_title = vacancy_data.title
    else:
        vacancy_title = "Данные отсутствуют."
        
    user_id = message.from_user.id
    bot = message.bot

    chat_group = ChatGroup.get()
    if not chat_group:
        await message.answer(exception_message)
        bot_logger.warning("⚠️ Админская группа не настроена.")
        return

    topic = Topic.get_by_user_id(user_id)

    try:
        # если топика нет в БД — создаём
        if not topic:
            forum_topic = await bot.create_forum_topic(chat_id=chat_group.group_id, name=str(user_id))
            topic = Topic.create(user_id=user_id, topic_id=forum_topic.message_thread_id)

        # --- 1. отправляем инфо-сообщение ---
        first_name = message.from_user.first_name or "Имя отсутствует"
        last_name = message.from_user.last_name or "Фамилия отсутствует"
        username = f"@{message.from_user.username}" if message.from_user.username else "Username отсутствует"

        await bot.send_message(
            chat_id=chat_group.group_id,
            message_thread_id=topic.topic_id,
            text=(
                f"📨 Сообщение от {first_name} {last_name} ({username}, ID: {user_id})\n"
                f"По вакансии: {vacancy_title}"
            )
        )

        # --- 2. копируем оригинальное сообщение пользователя ---
        await message.copy_to(
            chat_id=chat_group.group_id,
            message_thread_id=topic.topic_id
        )

    except TelegramBadRequest as e:
        # если топик удалили / message_thread_id не найден — пересоздаём
        text = str(e).lower()
        if any(word in text for word in ["message_thread_id", "thread", "not found", "topic"]):
            try:
                forum_topic = await bot.create_forum_topic(chat_id=chat_group.group_id, name=str(user_id))
                Topic.update_topic_id(user_id=user_id, new_topic_id=forum_topic.message_thread_id)

                await bot.send_message(
                    chat_id=chat_group.group_id,
                    message_thread_id=forum_topic.message_thread_id,
                    text=f"📨 Сообщение от {message.from_user.full_name} ({user_id}) по вакансии {vacancy_title}:"
                )
                await message.copy_to(
                    chat_id=chat_group.group_id,
                    message_thread_id=forum_topic.message_thread_id
                )
            except Exception as exception:
                bot_logger.warning(
                    f'❗ Ошибка при создании топика. Сообщение от {user_id} не доставлено. {exception}'
                )
                await message.answer(exception_message)
                return
        else:
            await message.answer(exception_message)
            return
    except Exception as exception:
        await message.answer(exception_message)
        bot_logger.warning(
            f'❗ Ошибка при доставке сообщения от {user_id}. {exception}'
        )
        return

    # подтверждение пользователю
    await message.answer("✅ Ваше сообщение отправлено менеджерам. Они ответят вам в ближайшее время.")
