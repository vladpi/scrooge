import logging
from typing import TYPE_CHECKING, Any, List, Mapping, Optional, TypeVar, cast

import asyncpg
import databases
import sqlalchemy as sa

from app.models.base import (
    BaseCreateRequest,
    BaseIdentity,
    BaseModel,
    BaseUpdateRequest,
)

from . import exceptions
from .base import MapperBase, RepositoryBase

_Model = TypeVar('_Model', bound=BaseModel)
_ModelCreate = TypeVar('_ModelCreate', bound=BaseCreateRequest)
_ModelUpdate = TypeVar('_ModelUpdate', bound=BaseUpdateRequest)
_ModelId = TypeVar('_ModelId', bound=BaseIdentity)


if TYPE_CHECKING:
    from databases.interfaces import Record

logger = logging.getLogger(__name__)


class DatabasesRepositoryImpl(  # noqa: WPS214
    RepositoryBase[_Model, _ModelId, _ModelCreate, _ModelUpdate],
):
    def __init__(self, db: databases.Database, mapper: MapperBase) -> None:
        self._db = db

        self._mapper = mapper
        self.DB_MODEL = mapper.__db_model__
        self.DB_MODEL_ID = getattr(self.DB_MODEL, mapper.__id_name__)
        self.DB_TABLE = self.DB_MODEL.__table__

    async def create(self, create_model: _ModelCreate) -> _Model:
        try:
            query = (
                self.DB_TABLE.insert()
                .values(create_model.dict(exclude_unset=True))
                .returning(self.DB_TABLE)
            )

            row = await self._db.fetch_one(query)
        except asyncpg.UniqueViolationError as err:
            raise exceptions.DuplicateError(err)
        except Exception as err:
            raise exceptions.CreateError(err)

        model = self.parse(row)
        if model is None:
            raise exceptions.MappingError()
        return model

    async def get(self, id_: _ModelId) -> _Model:
        query = self.DB_TABLE.select(self.DB_MODEL_ID == id_)
        return await self.find_one(query)

    async def update(self, id_: _ModelId, update_model: _ModelUpdate) -> _Model:
        try:
            query = (
                self.DB_TABLE.update()
                .where(self.DB_MODEL_ID == id_)
                .values(update_model.dict())
                .returning(self.DB_TABLE)
            )

            row = await self._db.fetch_one(query)
        except Exception as err:
            raise exceptions.UpdateError(err)

        model = self.parse(row)
        if model is None:
            raise exceptions.MappingError()
        return model

    async def delete(self, id_: _ModelId) -> None:
        try:
            query = self.DB_TABLE.delete(self.DB_MODEL_ID == id_)
            return await self._db.execute(query)
        except Exception as err:
            raise exceptions.RepositoryError(err)

    async def find_one(self, query: sa.sql.Select) -> _Model:
        query = query.limit(1)

        try:
            row = await self._db.fetch_one(query)
        except Exception as err:
            raise exceptions.RepositoryError(err)

        model = self.parse(row)
        if not model:
            raise exceptions.NotFoundError()

        return model

    async def find_many(self, query: sa.sql.Select) -> List[_Model]:
        try:
            rows = await self._db.fetch_all(query)
        except Exception as err:
            raise exceptions.RepositoryError(err)

        models = []
        for row in rows:
            model = self.parse(row)
            if model:
                models.append(model)
        return models

    def parse(self, row: Optional['Record']) -> Optional[_Model]:
        if not row:
            raise exceptions.NotFoundError()

        try:
            model = self._mapper.parse(cast(Mapping[str, Any], row))
        except Exception as err:
            logger.error(
                'Failed to parse model {0}. Error: {1}',
                self._mapper.__model__.__name__,
                err,
            )
            raise exceptions.MappingError(err)

        return model


class RelationalMapper(MapperBase):
    def parse(self, row: Mapping[str, Any]) -> BaseModel:
        return self.__model__(**row)
