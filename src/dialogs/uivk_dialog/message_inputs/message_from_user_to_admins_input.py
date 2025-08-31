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
    vacancy_data = Vacancy.get_by_id(vacancy_id=vacancy_id)
    user_question = (message.text or "").strip()
    if not user_question:
        await message.answer('🤔 Похоже, вы отправили что-то не то...')
        return

    user_id = message.from_user.id
    bot = message.bot

    chat_group = ChatGroup.get()
    if not chat_group:
        await message.answer(exception_message)
        bot_logger.warning(
            "⚠️ Админская группа не настроена. "
        )
        return

    topic = Topic.get_by_user_id(user_id)

    try:
        # если топика нет в БД — создаём
        if not topic:
            forum_topic = await bot.create_forum_topic(chat_id=chat_group.group_id, name=str(user_id))
            topic = Topic.create(user_id=user_id, topic_id=forum_topic.message_thread_id)

        # пытаемся отправить сообщение в топик
        first_name = message.from_user.first_name or "Имя отсутствует"
        last_name = message.from_user.last_name or "Фамилия отсутствует"
        username = f"@{message.from_user.username}" if message.from_user.username else "Username отсутствует"

        await bot.send_message(
            chat_id=chat_group.group_id,
            message_thread_id=topic.topic_id,
            text=(
                f"📨 Сообщение от {first_name} {last_name} ({username}, ID: {user_id})\n"
                f"По вакансии: {vacancy_data.title}\n\n"
                f"{user_question}"
            )
        )

    except TelegramBadRequest as e:
        # если топик удалили / message_thread_id не найден — пересоздаём и повторяем
        text = str(e).lower()
        if "message_thread_id" in text or "thread" in text or "not found" in text or "topic" in text:
            try:
                forum_topic = await bot.create_forum_topic(chat_id=chat_group.group_id, name=str(user_id))
                Topic.update_topic_id(user_id=user_id, new_topic_id=forum_topic.message_thread_id)

                await bot.send_message(
                    chat_id=chat_group.group_id,
                    message_thread_id=forum_topic.message_thread_id,
                    text=f"📨 Сообщение от {message.from_user.full_name} ({user_id}) по вакансии {vacancy_data.title}:\n\n{user_question}"
                )
            except Exception as exception:
                bot_logger.warning(
                    f'❗ Не удалось доставить сообщение администраторам. Ошибка при создании топика. {user_id} {exception}'
                )
                await message.answer(exception_message)
                return
        else:
            await message.answer(exception_message)
            return
    except Exception as exception:
        await message.answer(exception_message)
        bot_logger.warning(
            f'❗ Не удалось доставить сообщение администраторам. Ошибка при создании топика. {user_id} {exception}'
        )
        return

    # подтверждение пользователю
    await message.answer("✅ Ваше сообщение отправлено мененджерам. Они ответят вам в ближайшее время.")
