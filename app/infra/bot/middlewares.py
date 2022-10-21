from typing import TYPE_CHECKING

from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from app import models
from app.domains import CreateOrUpdateTelegramUserRequest

if TYPE_CHECKING:
    from .context import Context

CTX_ATTR = 'ctx'
USER_ATTR = 'user'
WORKSPACE_ATTR = 'workspace'


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


class UserMiddleware(BaseMiddleware):
    async def on_process_message(
        self,
        message: types.Message,
        data: dict,  # noqa: WPS110
    ) -> None:
        data[USER_ATTR] = await self._fetch_user(
            message.bot.data[CTX_ATTR],
            message.from_user,
        )

    async def on_process_callback_query(
        self,
        callback_query: types.Message,
        data: dict,  # noqa: WPS110
    ) -> None:
        data[USER_ATTR] = await self._fetch_user(
            callback_query.bot.data[CTX_ATTR],
            callback_query.from_user,
        )

    async def _fetch_user(self, ctx: 'Context', from_user: types.User) -> models.TelegramUser:
        return await ctx.services.users.create_or_update_user_from_telegram(
            CreateOrUpdateTelegramUserRequest(
                telegram_user_id=from_user.id,
                username=from_user.username,
                first_name=from_user.first_name,
                last_name=from_user.last_name,
            ),
        )


class WorkspaceMiddleware(BaseMiddleware):
    async def on_process_message(
        self,
        message: types.Message,
        data: dict,  # noqa: WPS110
    ) -> None:
        data[WORKSPACE_ATTR] = await self._get_workspace(
            message.bot.data[CTX_ATTR],
            message.from_user,
        )

    async def on_process_callback_query(
        self,
        callback_query: types.Message,
        data: dict,  # noqa: WPS110
    ) -> None:
        data[WORKSPACE_ATTR] = await self._get_workspace(
            callback_query.bot.data[CTX_ATTR],
            callback_query.from_user,
        )

    async def _get_workspace(
        self,
        ctx: 'Context',
        from_user: types.User,
    ) -> models.Workspace:
        telegram_user = await ctx.services.users.get_user_from_telegram(from_user.id)

        return await ctx.services.workspaces.get_user_workspace(telegram_user.user_id)
