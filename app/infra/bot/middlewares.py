from typing import Any, Awaitable, Callable

from aiogram.types import TelegramObject, Update, User
from neoteroi import di

from app import domains, models

CONTAINER_ATTR = 'container'
USER_ATTR = 'user'
WORKSPACE_ATTR = 'workspace'

_AiogramHandler = Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]]  # noqa: WPS221


class BaseMiddleware:
    def __init__(self, container: di.Container) -> None:
        super().__init__()
        self._container = container


class CtxMiddleware(BaseMiddleware):
    async def __call__(
        self,
        update_handler: _AiogramHandler,
        update: Update,
        update_data: dict[str, Any],
    ) -> Any:
        update_data[CONTAINER_ATTR] = self._container

        await update_handler(update, update_data)


class UserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        update_handler: _AiogramHandler,
        update: Update,
        update_data: dict[str, Any],
    ) -> Any:
        if update.message is not None:
            from_user = update.message.from_user
        elif update.callback_query is not None:
            from_user = update.callback_query.from_user
        else:
            raise RuntimeError(f'Unsupported event {update.event_type} for UserMiddleware')

        if from_user is not None:
            update_data[USER_ATTR] = await self._fetch_user(from_user)

        await update_handler(update, update_data)

    async def _fetch_user(self, from_user: User) -> models.TelegramUser:
        users_service = self._container.resolve(domains.UsersService)

        return await users_service.create_or_update_user_from_telegram(
            domains.CreateOrUpdateTelegramUserRequest(
                telegram_user_id=from_user.id,
                username=from_user.username,
                first_name=from_user.first_name,
                last_name=from_user.last_name,
            ),
        )


class WorkspaceMiddleware(BaseMiddleware):
    async def __call__(
        self,
        update_handler: _AiogramHandler,
        update: Update,
        update_data: dict[str, Any],
    ) -> Any:
        if update.message is not None:
            from_user = update.message.from_user
        elif update.callback_query is not None:
            from_user = update.callback_query.from_user
        else:
            raise RuntimeError(f'Unsupported event {update.event_type} for UserMiddleware')

        if from_user is not None:
            update_data[WORKSPACE_ATTR] = await self._get_workspace(from_user)

        await update_handler(update, update_data)

    async def _get_workspace(
        self,
        from_user: User,
    ) -> models.Workspace:
        users_service = self._container.resolve(domains.UsersService)
        workspaces_service = self._container.resolve(domains.WorkspacesService)

        telegram_user = await users_service.get_user_from_telegram(from_user.id)

        return await workspaces_service.get_user_workspace(telegram_user.user_id)
