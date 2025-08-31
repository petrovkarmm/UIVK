import datetime
import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import DefaultKeyBuilder
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import ErrorEvent, Message
from aiogram_dialog import setup_dialogs, DialogManager, ShowMode
from aiogram_dialog.api.exceptions import UnknownIntent, OutdatedIntent

from src.database.dataclasses.chat_group import ChatGroup
from src.database.dataclasses.vacancy import Vacancy
from src.dialogs.admin_panel_dialog.admin_panel_dialog_router import admin_panel_dialog_router
from src.dialogs.uivk_dialog.uivk_dialog_router import uivk_dialog_router
from src.dialogs.uivk_dialog.uivk_dialog_states import UivkDialogStatesGroup
from src.middlewares.logger_middleware import GlobalLogger
from src.routers.admin.handlers import admin_panel
from src.routers.user.handlers import start_router
from src.logs.logger import bot_logger
from src.settings import redis_connect_url, DEBUG, bot_test_token, bot_token


async def bot_start():
    if DEBUG:
        dp = Dispatcher()
        bot = Bot(token=bot_test_token)
    else:
        storage = RedisStorage.from_url(
            redis_connect_url, key_builder=DefaultKeyBuilder(with_destiny=True)
        )
        dp = Dispatcher(storage=storage)
        bot = Bot(token=bot_token)

    async def error_unknown_intent_handler(event: ErrorEvent, dialog_manager: DialogManager):
        """Обработка ошибок UnknownIntent / OutdatedIntent"""
        query = event.update.callback_query

        exception = event.exception

        if isinstance(exception, TelegramBadRequest) and "wrong remote file identifier" in str(exception):
            bot_logger.warning("❌ Недействительный file_id.")

            await bot.send_message(
                chat_id=query.message.chat.id,
                text=(
                    "⚠️ Ой! Не удалось загрузить вопрос.\n\n"
                    "Мы уже автоматически оповестили наших HR-менеджеров об этой ошибке. "
                    "Если в ближайшее время проблема не исчезнет — пожалуйста, сообщите нам напрямую через HeadHunter. 🙏"
                ),
                parse_mode=ParseMode.HTML,
            )

            chat_group = ChatGroup.get()
            if not chat_group:
                bot_logger.warning(
                    "⚠️ Админская группа не настроена. "
                )
            else:
                vacancy_id = dialog_manager.dialog_data['vacancy_id']
                vacancy_data = Vacancy.get_by_id(vacancy_id=vacancy_id)

                await bot.send_message(
                    chat_id=chat_group.group_id,
                    text=(
                        f"⚠️ Обнаружена ошибка в вакансии <b>{vacancy_data.title}</b>.\n\n"
                        f"В одном из FAQ с медиа прикреплён нерабочий файл. "
                        f"Пожалуйста, удалите этот FAQ и создайте его заново с корректным вложением."
                    ),
                    parse_mode="HTML",
                )

                await dialog_manager.switch_to(
                    UivkDialogStatesGroup.uivk_vacancy_and_questions
                )

        if not isinstance(exception, (UnknownIntent, OutdatedIntent)):
            bot_logger.warning(f"Необработанная ошибка: {exception}")
        else:
            # Пытаемся удалить сообщение с "битой" callback-кнопкой
            try:
                await bot.delete_message(
                    chat_id=query.message.chat.id,
                    message_id=query.message.message_id,
                )
                await bot.send_message(
                    chat_id=query.message.chat.id,
                    text="⚠️ Упс! Кажется, что-то пошло не так.",
                    parse_mode=ParseMode.HTML,
                )
            except AttributeError:
                bot_logger.warning("Ошибка: callback пришёл в закрытый диалог")
            except Exception as exception:
                bot_logger.warning(f"Ошибка при удалении/отправке сообщения: {exception}")

        # Восстанавливаем пользователя в дефолтное меню
        try:
            await dialog_manager.reset_stack()
            await dialog_manager.start(UivkDialogStatesGroup.uivk_start_menu, show_mode=ShowMode.SEND)
        except Exception as exception:
            bot_logger.warning(f"Ошибка при восстановлении стека диалога: {exception}")

    @dp.message(F.text == 'ping')
    async def full_restart(message: Message, state: FSMContext, dialog_manager: DialogManager):
        await message.answer(
            text='pong'
        )

    @dp.message(Command('id'))
    async def get_user_id(message: Message):
        await message.answer(
            text=f'Ваш ID: {message.from_user.id}'
        )

    @dp.message(Command('id_group'))
    async def get_chat_id_user(message: Message):
        await message.answer(
            text=f'ID группы: {message.chat.id}'
        )

    # error handler
    dp.errors.register(error_unknown_intent_handler)

    # logger mw
    dp.callback_query.middleware.register(GlobalLogger())

    setup_dialogs(dp)
    dp.include_router(admin_panel)
    dp.include_router(admin_panel_dialog_router)
    dp.include_router(uivk_dialog_router)
    dp.include_router(start_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        bot_logger.info(
            f'Старт бота - {datetime.datetime.now()}'
        )
        asyncio.run(bot_start())
    except Exception as e:
        bot_logger.warning(e)
