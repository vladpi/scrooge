import logging
from typing import Generic, TypeVar

import sqlalchemy as sa
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncEngine

from app.models.base import (
    BaseCreateRequest,
    BaseIdentity,
    BaseModel,
    BaseUpdateRequest,
)

from . import exceptions
from .base import MapperBase

_Model = TypeVar('_Model', bound=BaseModel)
_ModelCreate = TypeVar('_ModelCreate', bound=BaseCreateRequest)
_ModelUpdate = TypeVar('_ModelUpdate', bound=BaseUpdateRequest)
_ModelId = TypeVar('_ModelId', bound=BaseIdentity)


logger = logging.getLogger(__name__)


class SQLAlchemyRepository(Generic[_Model, _ModelId, _ModelCreate, _ModelUpdate]):
    def __init__(self, db_engine: AsyncEngine, mapper: MapperBase) -> None:
        self._db_engine = db_engine

        self._mapper = mapper
        self.DB_MODEL = mapper.__db_model__
        self.DB_MODEL_ID = getattr(self.DB_MODEL, mapper.__id_name__)

    async def create(self, create_model: _ModelCreate) -> _Model:
        async with self._db_engine.begin() as conn:
            query = (
                sa.insert(self.DB_MODEL)
                .values(create_model.dict(exclude_none=True))
                .returning(self.DB_MODEL)
            )

            try:
                result = await conn.execute(query)
                row = result.one()
            # FIXME
            # except asyncpg.UniqueViolationError as err:
            # raise exceptions.DuplicateError(err)
            except Exception as err:
                raise exceptions.CreateError(err)

        model = self.parse(row)
        if model is None:
            raise exceptions.MappingError()
        return model

    async def get(self, id_: _ModelId) -> _Model:
        query = sa.select(self.DB_MODEL).where(self.DB_MODEL_ID == id_)
        return await self.fetch_one(query)

    async def update(self, id_: _ModelId, update_model: _ModelUpdate) -> _Model:
        async with self._db_engine.begin() as conn:
            query = (
                sa.update(self.DB_MODEL)
                .where(self.DB_MODEL_ID == id_)
                .values(update_model.dict(exclude_unset=True))
                .returning(self.DB_MODEL)
            )

            try:
                result = await conn.execute(query)
                row = result.one()
            except Exception as err:
                raise exceptions.UpdateError(err)

        return self.parse(row)

    async def delete(self, id_: _ModelId) -> None:
        query = sa.delete(self.DB_MODEL).where(self.DB_MODEL_ID == id_)
        async with self._db_engine.begin() as conn:
            try:
                await conn.execute(query)
            except Exception as err:
                raise exceptions.RepositoryError(err)

    async def fetch_one(self, query: sa.sql.Select | sa.sql.Update) -> _Model:
        async with self._db_engine.begin() as conn:
            try:
                result = await conn.execute(query)
                row = result.one()
            except NoResultFound:
                raise exceptions.NotFoundError()
            except Exception as err:
                raise exceptions.RepositoryError(err)

        return self.parse(row)

    async def fetch_many(self, query: sa.sql.Select) -> list[_Model]:
        async with self._db_engine.begin() as conn:
            try:
                result = await conn.execute(query)
                rows = result.all()
            except Exception as err:
                raise exceptions.RepositoryError(err)

        return [self.parse(row) for row in rows]

    def parse(self, row: sa.Row) -> _Model:
        try:
            model = self._mapper.parse(row)
        except Exception as err:
            logger.error(
                'Failed to parse model {0}. Error: {1}',
                self._mapper.__model__.__name__,
                err,
            )
            raise exceptions.MappingError(err)

        return model


class RelationalMapper(MapperBase):
    def parse(self, row: sa.Row) -> BaseModel:
        return self.__model__(**row._asdict())
