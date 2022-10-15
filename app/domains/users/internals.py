import logging

from app import models, repositories
from app.domains import CreateWorkspaceRequest, create_workspace

from .schemas import CreateOrUpdateTelegramUserRequest

logger = logging.getLogger(__name__)


async def create_or_update_user_from_telegram(
    repos: repositories.Repositories,
    request: CreateOrUpdateTelegramUserRequest,
) -> models.TelegramUser:
    try:
        telegram_user = await repos.telegram_users_repo.get(request.telegram_user_id)
        return await repos.telegram_users_repo.update(
            telegram_user.id,
            models.TelegramUserUpdate(
                username=request.username,
                first_name=request.first_name,
                last_name=request.last_name,
            ),
        )
    except repositories.NotFoundError:
        logger.info(f'Not found Telegram User with id#{request.telegram_user_id} – creating new')

    return await create_user_from_telegram(
        repos,
        request,
    )


async def create_user_from_telegram(
    repos: repositories.Repositories,
    request: CreateOrUpdateTelegramUserRequest,
) -> models.TelegramUser:
    # TODO transaction and error handling
    user = await repos.users_repo.create(models.UserCreate())
    telegram_user = await repos.telegram_users_repo.create(
        models.TelegramUserCreate(
            id=request.telegram_user_id,
            user_id=user.id,
            username=request.username,
            first_name=request.first_name,
            last_name=request.last_name,
        ),
    )

    await create_workspace(
        repos,
        CreateWorkspaceRequest(owner_id=user.id, init_defaults=True),
    )

    return telegram_user


async def get_user_from_telegram(
    repos: repositories.Repositories,
    id_: models.TelegramUserId,
) -> models.TelegramUser:
    return await repos.telegram_users_repo.get(id_)
