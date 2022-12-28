import abc
import logging
from decimal import Decimal
from typing import List

import databases
import sqlalchemy as sa

from app import db, models

from .base import RepositoryBase
from .exceptions import MappingError, UpdateError
from .sql import DatabasesRepositoryImpl, RelationalMapper

logger = logging.getLogger(__name__)


class _AccountsMapper(RelationalMapper):
    __model__ = models.Account
    __db_model__ = db.Account


class AccountsRepository(  # noqa: B024 FIXME
    RepositoryBase[
        models.Account,
        models.AccountId,
        models.AccountCreate,
        models.AccountUpdate,
    ],
    abc.ABC,
):
    """Abstract Categories Repository"""

    async def update_balance(self, id_: models.AccountId, diff: Decimal) -> models.Account:
        raise NotImplementedError

    async def get_by_workspace_id(self, workspace_id: models.WorkspaceId) -> List[models.Account]:
        raise NotImplementedError

    async def get_by_workspace_id_and_name(
        self,
        workspace_id: models.WorkspaceId,
        name: str,
    ) -> models.Account:
        raise NotImplementedError


class AccountsRepositoryImpl(AccountsRepository):  # noqa: WPS214
    def __init__(self, db_conn: databases.Database) -> None:
        self._conn = db_conn
        self._impl: DatabasesRepositoryImpl = DatabasesRepositoryImpl(db_conn, _AccountsMapper())

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
            sa.update(db.Account.__table__)
            .values(balance=db.Account.balance + diff)
            .where(db.Account.id == id_)
            .returning(db.Account.__table__)
        )

        # FIXME better errors handling
        try:
            row = await self._conn.fetch_one(query)
        except Exception as ex:
            raise UpdateError(ex)

        account = self._impl.parse(row)
        if account is None:
            raise MappingError()

        return account

    async def get_by_workspace_id(self, workspace_id: models.WorkspaceId) -> List[models.Account]:
        query = sa.select([db.Account.__table__]).where(
            db.Account.workspace_id == workspace_id,
        )
        return await self._impl.find_many(query)

    async def get_by_workspace_id_and_name(
        self,
        workspace_id: models.WorkspaceId,
        name: str,
    ) -> models.Account:
        query = sa.select([db.Account.__table__]).where(
            sa.and_(
                db.Account.workspace_id == workspace_id,
                db.Account.name == name,
            ),
        )
        return await self._impl.find_one(query)
