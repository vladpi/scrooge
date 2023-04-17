import logging
from typing import Protocol

from sqlalchemy.ext.asyncio import AsyncEngine

from app import db, models

from .sql import RelationalMapper, SQLAlchemyRepository

logger = logging.getLogger(__name__)


class _UsersMapper(RelationalMapper):
    __model__ = models.User
    __db_model__ = db.User


class UsersRepository(Protocol):
    async def create(self, create_model: models.UserCreate) -> models.User:
        ...

    async def get(self, id_: models.UserId) -> models.User:
        ...

    async def update(
        self,
        id_: models.UserId,
        update_model: models.UserUpdate,
    ) -> models.User:
        ...

    async def delete(self, id_: models.UserId) -> None:
        ...


class UsersRepositoryImpl(UsersRepository):
    def __init__(self, db_engine: AsyncEngine) -> None:
        self._impl: SQLAlchemyRepository[
            models.User,
            models.UserId,
            models.UserCreate,
            models.UserUpdate,
        ] = SQLAlchemyRepository(db_engine=db_engine, mapper=_UsersMapper())

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


class TelegramUsersRepository(Protocol):
    async def create(self, create_model: models.TelegramUserCreate) -> models.TelegramUser:
        ...

    async def get(self, id_: models.TelegramUserId) -> models.TelegramUser:
        ...

    async def update(
        self,
        id_: models.TelegramUserId,
        update_model: models.TelegramUserUpdate,
    ) -> models.TelegramUser:
        ...

    async def delete(self, id_: models.TelegramUserId) -> None:
        ...


class TelegramUsersRepositoryImpl(TelegramUsersRepository):
    def __init__(self, db_engine: AsyncEngine) -> None:
        self._impl: SQLAlchemyRepository[
            models.TelegramUser,
            models.TelegramUserId,
            models.TelegramUserCreate,
            models.TelegramUserUpdate,
        ] = SQLAlchemyRepository(db_engine=db_engine, mapper=_TelegramUsersMapper())

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
