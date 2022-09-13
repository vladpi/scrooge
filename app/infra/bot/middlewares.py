from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

CTX_ATTR = 'ctx'


class CtxMiddleware(BaseMiddleware):
    async def on_process_message(
        self,
        message: types.Message,
        data: dict,  # noqa: WPS110
    ) -> None:
        data[CTX_ATTR] = message.bot.data[CTX_ATTR]

    async def on_process_callback_query(
        self,
        callback_query: types.CallbackQuery,
        data: dict,  # noqa: WPS110
    ) -> None:
        data[CTX_ATTR] = callback_query.bot.data[CTX_ATTR]
