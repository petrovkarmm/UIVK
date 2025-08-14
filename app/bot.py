import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import DefaultKeyBuilder
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import ErrorEvent, Message
from aiogram_dialog import setup_dialogs, DialogManager
from aiogram_dialog.api.exceptions import UnknownIntent, OutdatedIntent

from app.dialogs.admin_panel_dialog.admin_panel_dialog_router import admin_panel_dialog_router
from app.dialogs.uivk_dialog.uivk_dialog_router import uivk_dialog_router
from app.routers.admin_panel.handlers import admin_panel
from app.routers.start.handlers import start_router
from app.logs.logger import bot_logger
from app.settings import redis_connect_url, DEBUG, bot_test_token, bot_token


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

    async def error_unknown_intent_handler(
            event: ErrorEvent, dialog_manager: DialogManager
    ):
        if isinstance(event.exception, UnknownIntent) or isinstance(event.exception, OutdatedIntent):
            try:
                event_message_id = event.update.callback_query.message.message_id
                event_chat_id = event.update.callback_query.message.chat.id
                await bot.delete_message(
                    chat_id=event_chat_id, message_id=event_message_id
                )
                await bot.send_message(
                    text='⚠️ Упс! Кажется, что-то пошло не так.',
                    chat_id=event_chat_id,
                    parse_mode=ParseMode.HTML
                )
            except AttributeError as exception:
                bot_logger.warning(f'Отбилась в закрытый диалог.', exception)
            except Exception as exception:
                bot_logger.warning(exception)
        else:
            bot_logger.warning(f"{event.exception}")

    @dp.message(F.text == 'ping')
    async def full_restart(message: Message, state: FSMContext, dialog_manager: DialogManager):
        await message.answer(
            text='pong'
        )

    # error handler
    # dp.errors.register(error_unknown_intent_handler)

    # logger mw
    # dp.callback_query.middleware.register(GlobalLogger())

    # default routers
    dp.include_router(admin_panel)
    dp.include_router(start_router)

    # dialogs routers
    setup_dialogs(dp)
    dp.include_router(uivk_dialog_router)
    dp.include_router(admin_panel_dialog_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        bot_logger.info(
            'Старт бота.'
        )
        # create_tables()
        # insert_values()
        asyncio.run(bot_start())
    except Exception as e:
        bot_logger.warning(e)
