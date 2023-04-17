import logging
from decimal import Decimal
from typing import List, Protocol

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncEngine

from app import db, models

from .exceptions import UpdateError
from .sql import RelationalMapper, SQLAlchemyRepository

logger = logging.getLogger(__name__)


class _AccountsMapper(RelationalMapper):
    __model__ = models.Account
    __db_model__ = db.Account


class AccountsRepository(Protocol):
    async def create(self, create_model: models.AccountCreate) -> models.Account:
        ...

    async def get(self, id_: models.AccountId) -> models.Account:
        ...

    async def update(
        self,
        id_: models.AccountId,
        update_model: models.AccountUpdate,
    ) -> models.Account:
        ...

    async def delete(self, id_: models.AccountId) -> None:
        ...

    async def update_balance(self, id_: models.AccountId, diff: Decimal) -> models.Account:
        ...

    async def get_by_workspace_id(self, workspace_id: models.WorkspaceId) -> List[models.Account]:
        ...

    async def get_by_workspace_id_and_name(
        self,
        workspace_id: models.WorkspaceId,
        name: str,
    ) -> models.Account:
        ...


class AccountsRepositoryImpl(AccountsRepository):  # noqa: WPS214
    def __init__(self, db_engine: AsyncEngine) -> None:
        self._impl: SQLAlchemyRepository[
            models.Account,
            models.AccountId,
            models.AccountCreate,
            models.AccountUpdate,
        ] = SQLAlchemyRepository(db_engine=db_engine, mapper=_AccountsMapper())

    async def create(self, create_model: models.AccountCreate) -> models.Account:
        return await self._impl.create(create_model)

    async def get(self, id_: models.AccountId) -> models.Account:
        return await self._impl.get(id_)

    async def update(
        self,
        id_: models.AccountId,
        update_model: models.AccountUpdate,
    ) -> models.Account:
        return await self._impl.update(id_, update_model)

    async def delete(self, id_: models.AccountId) -> None:
        return await self._impl.delete(id_)

    async def update_balance(self, id_: models.AccountId, diff: Decimal) -> models.Account:
        query = (
            sa.update(db.Account)
            .values(balance=db.Account.balance + diff)
            .where(db.Account.id == id_)
            .returning(db.Account.__table__)
        )

        # FIXME better errors handling
        try:
            return await self._impl.fetch_one(query)
        except Exception as ex:
            raise UpdateError(ex)

    async def get_by_workspace_id(self, workspace_id: models.WorkspaceId) -> List[models.Account]:
        query = sa.select(db.Account).where(db.Account.workspace_id == workspace_id)
        return await self._impl.fetch_many(query)

    async def get_by_workspace_id_and_name(
        self,
        workspace_id: models.WorkspaceId,
        name: str,
    ) -> models.Account:
        query = sa.select(db.Account).where(
            sa.and_(
                db.Account.workspace_id == workspace_id,
                db.Account.name == name,
            ),
        )
        return await self._impl.fetch_one(query)
