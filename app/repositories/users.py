import abc
import logging

import databases

from app import db, models

from .base import RepositoryBase
from .sql import DatabasesRepositoryImpl, RelationalMapper

logger = logging.getLogger(__name__)


class _UsersMapper(RelationalMapper):
    __model__ = models.User
    __db_model__ = db.User


class UsersRepository(  # noqa: B024 FIXME
    RepositoryBase[
        models.User,
        models.UserId,
        models.UserCreate,
        models.UserUpdate,
    ],
    abc.ABC,
):
    """Abstract User Repository"""


class UsersRepositoryImpl(UsersRepository):
    def __init__(self, db_conn: databases.Database) -> None:
        self._impl: DatabasesRepositoryImpl = DatabasesRepositoryImpl(db_conn, _UsersMapper())

    async def create(self, create_model: models.UserCreate) -> models.User:
        return await self._impl.create(create_model)

    async def get(self, id_: models.UserId) -> models.User:
        return await self._impl.get(id_)

    async def update(
        self,
        id_: models.UserId,
        update_model: models.UserUpdate,
    ) -> models.User:
        return await self._impl.update(id_, update_model)

    async def delete(self, id_: models.UserId) -> None:
        return await self._impl.delete(id_)


class _TelegramUsersMapper(RelationalMapper):
    __model__ = models.TelegramUser
    __db_model__ = db.TelegramUser


class TelegramUsersRepository(  # noqa: B024 FIXME
    RepositoryBase[
        models.TelegramUser,
        models.TelegramUserId,
        models.TelegramUserCreate,
        models.TelegramUserUpdate,
    ],
    abc.ABC,
):
    """Abstract Telegram User Repository"""


class TelegramUsersRepositoryImpl(TelegramUsersRepository):
    def __init__(self, db_conn: databases.Database) -> None:
        self._impl: DatabasesRepositoryImpl = DatabasesRepositoryImpl(
            db_conn,
            _TelegramUsersMapper(),
        )

    async def create(self, create_model: models.TelegramUserCreate) -> models.TelegramUser:
        return await self._impl.create(create_model)

    async def get(self, id_: models.TelegramUserId) -> models.TelegramUser:
        return await self._impl.get(id_)

    async def update(
        self,
        id_: models.TelegramUserId,
        update_model: models.TelegramUserUpdate,
    ) -> models.TelegramUser:
        return await self._impl.update(id_, update_model)

    async def delete(self, id_: models.TelegramUserId) -> None:
        return await self._impl.delete(id_)
