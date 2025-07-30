import asyncio
from typing import Any, Callable, Dict, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from app.logs.logger import handler_log


class GlobalLogger(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        dialog_ctx = data["aiogd_context"]
        event_ctx = data["aiogd_event_context"]

        user = event_ctx.user

        state = dialog_ctx.state
        start_data = dialog_ctx.start_data
        dialog_data = dialog_ctx.dialog_data

        logger_task = asyncio.create_task(
            handler_log(
                user=user, state=state, start_data=start_data, dialog_data=dialog_data
            )
        )

        handler_task = asyncio.create_task(handler(event, data))

        await asyncio.gather(handler_task, logger_task)
        return handler_task
