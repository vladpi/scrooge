import abc
import logging
from decimal import Decimal
from typing import TYPE_CHECKING

import sqlalchemy as sa

from app import db, models

from .base import RepositoryBase
from .exceptions import MappingError, UpdateError
from .sql import DatabasesRepositoryImpl, RelationalMapper

if TYPE_CHECKING:
    from databases import Database

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


class AccountsRepositoryImpl(AccountsRepository):
    def __init__(self, db_conn: 'Database') -> None:
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
