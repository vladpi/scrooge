import logging
from typing import Protocol

from sqlalchemy.ext.asyncio import AsyncEngine

from app import db, models

from .sql import RelationalMapper, SQLAlchemyRepository

logger = logging.getLogger(__name__)


class _TransactionsMapper(RelationalMapper):
    __model__ = models.Transaction
    __db_model__ = db.Transaction


class TranasactionssRepository(Protocol):
    async def create(self, create_model: models.TransactionCreate) -> models.Transaction:
        ...

    async def get(self, id_: models.TransactionId) -> models.Transaction:
        ...

    async def update(
        self,
        id_: models.TransactionId,
        update_model: models.TransactionUpdate,
    ) -> models.Transaction:
        ...

    async def delete(self, id_: models.TransactionId) -> None:
        ...


class TransactionsRepositoryImpl(TranasactionssRepository):
    def __init__(self, db_engine: AsyncEngine) -> None:
        self._impl: SQLAlchemyRepository[
            models.Transaction,
            models.TransactionId,
            models.TransactionCreate,
            models.TransactionUpdate,
        ] = SQLAlchemyRepository(db_engine=db_engine, mapper=_TransactionsMapper())

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
