import abc
import logging

import databases

from app import db, models

from .base import RepositoryBase
from .sql import DatabasesRepositoryImpl, RelationalMapper

logger = logging.getLogger(__name__)


class _TransactionsMapper(RelationalMapper):
    __model__ = models.Transaction
    __db_model__ = db.Transaction


class TranasactionssRepository(  # noqa: B024 FIXME
    RepositoryBase[
        models.Transaction,
        models.TransactionId,
        models.TransactionCreate,
        models.TransactionUpdate,
    ],
    abc.ABC,
):
    """Abstract Categories Repository"""


class TransactionsRepositoryImpl(TranasactionssRepository):
    def __init__(self, db_conn: databases.Database) -> None:
        self._impl: DatabasesRepositoryImpl = DatabasesRepositoryImpl(
            db_conn,
            _TransactionsMapper(),
        )

    async def create(self, create_model: models.TransactionCreate) -> models.Transaction:
        return await self._impl.create(create_model)

    async def get(self, id_: models.TransactionId) -> models.Transaction:
        return await self._impl.get(id_)

    async def update(
        self,
        id_: models.TransactionId,
        update_model: models.TransactionUpdate,
    ) -> models.Transaction:
        return await self._impl.update(id_, update_model)

    async def delete(self, id_: models.TransactionId) -> None:
        return await self._impl.delete(id_)
