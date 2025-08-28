import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import DefaultKeyBuilder
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import ErrorEvent, Message
from aiogram_dialog import setup_dialogs, DialogManager
from aiogram_dialog.api.exceptions import UnknownIntent, OutdatedIntent

from app.database.dataclasses.admin_dataclass import Admin
from app.dialogs.admin_panel_dialog.admin_panel_dialog_router import admin_panel_dialog_router
from app.dialogs.uivk_dialog.uivk_dialog_router import uivk_dialog_router
from app.routers.admin_panel.filters import IsAdminFilter
from app.routers.admin_panel.handlers import admin_panel
from app.routers.start.handlers import start_router
from app.logs.logger import bot_logger
from app.settings import redis_connect_url, DEBUG, bot_test_token, bot_token, super_admins


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

    @dp.message(Command('id'))
    async def get_user_id(message: Message, state: FSMContext, dialog_manager: DialogManager):
        await message.answer(
            text=f'Ваш ID: {message.from_user.id}'
        )

    @dp.message(IsAdminFilter(), Command("add"))
    async def add_new_admin(message: Message, state: FSMContext, dialog_manager: DialogManager, command: CommandObject):
        try:
            new_admin_telegram_id = int(command.args.strip())
        except (ValueError, AttributeError):
            await message.answer("Укажите корректный Telegram ID: /add <id>")
            return

        if Admin.add(new_admin_telegram_id):
            await message.answer(f"✅ Админ с ID {new_admin_telegram_id} успешно добавлен.")
        else:
            await message.answer(f"⚠️ Админ с ID {new_admin_telegram_id} уже есть в базе.")

    @dp.message(IsAdminFilter(), Command("remove"))
    async def delete_admin(message: Message, state: FSMContext, dialog_manager: DialogManager, command: CommandObject):
        try:
            admin_telegram_id = int(command.args.strip())
        except (ValueError, AttributeError):
            await message.answer("Укажите корректный Telegram ID: /remove <id>")
            return

        if Admin.delete(admin_telegram_id):
            await message.answer(f"🗑 Админ с ID {admin_telegram_id} удалён.")
        else:
            await message.answer(f"❌ Админ с ID {admin_telegram_id} не найден в базе.")

    @admin_panel.message(IsAdminFilter(), Command("list_admins"))
    async def list_admins_handler(message: Message):

        # Обычные админы из базы (set, чтобы быстро убирать дубли)
        db_admins = {str(admin.telegram_id) for admin in Admin.all()}

        # Исключаем дубли — супер-админов не дублируем в "обычных"
        db_admins -= super_admins

        def format_block(title: str, ids: set[str], emoji: str) -> str:
            if ids:
                return f"{emoji} <b>{title}</b>:\n" + "\n".join(f"• <code>{i}</code>" for i in sorted(ids)) + "\n\n"
            return f"{emoji} <b>{title}</b>: (нет)\n\n"

        response = (
                "👑 <b>Список администраторов</b>\n\n"
                + format_block("Супер-админы", super_admins, "✨")
                + format_block("Админы", db_admins, "🛡")
        )

        await message.answer(response.strip(), parse_mode="HTML")

    # error handler
    # dp.errors.register(error_unknown_intent_handler)

    # logger mw
    # dp.callback_query.middleware.register(GlobalLogger())

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
            'Старт бота.'
        )
        # create_tables()
        # insert_values()
        asyncio.run(bot_start())
    except Exception as e:
        bot_logger.warning(e)
