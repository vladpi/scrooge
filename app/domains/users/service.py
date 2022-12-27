import logging

from app import models, repositories

from .schemas import CreateOrUpdateTelegramUserRequest

logger = logging.getLogger(__name__)


class UsersService:
    def __init__(
        self,
        users_repo: repositories.UsersRepository,
        telegram_users_repo: repositories.TelegramUsersRepository,
    ) -> None:
        self._users_repo = users_repo
        self._telegram_users_repo = telegram_users_repo

    async def create_or_update_user_from_telegram(
        self,
        request: CreateOrUpdateTelegramUserRequest,
    ) -> models.TelegramUser:
        try:
            telegram_user = await self._telegram_users_repo.get(request.telegram_user_id)
            return await self._telegram_users_repo.update(
                telegram_user.id,
                models.TelegramUserUpdate(
                    username=request.username,
                    first_name=request.first_name,
                    last_name=request.last_name,
                ),
            )
        except repositories.NotFoundError:
            logger.info(
                f'Not found Telegram User with id#{request.telegram_user_id} – creating new',
            )

        return await self.create_user_from_telegram(request)

    async def create_user_from_telegram(
        self,
        request: CreateOrUpdateTelegramUserRequest,
    ) -> models.TelegramUser:
        # TODO transaction and error handling
        user = await self._users_repo.create(models.UserCreate())
        return await self._telegram_users_repo.create(
            models.TelegramUserCreate(
                id=request.telegram_user_id,
                user_id=user.id,
                username=request.username,
                first_name=request.first_name,
                last_name=request.last_name,
            ),
        )

        # FIXME create workspace here or not ?

    async def get_user_from_telegram(
        self,
        id_: models.TelegramUserId,
    ) -> models.TelegramUser:
        return await self._telegram_users_repo.get(id_)
