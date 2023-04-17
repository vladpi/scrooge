import logging
from typing import Protocol

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncEngine

from app import db, models

from .sql import RelationalMapper, SQLAlchemyRepository

logger = logging.getLogger(__name__)


class _CategoriesMapper(RelationalMapper):
    __model__ = models.Category
    __db_model__ = db.Category


class CategoriesRepository(Protocol):
    async def create(self, create_model: models.CategoryCreate) -> models.Category:
        ...

    async def get(self, id_: models.CategoryId) -> models.Category:
        ...

    async def update(
        self,
        id_: models.CategoryId,
        update_model: models.CategoryUpdate,
    ) -> models.Category:
        ...

    async def delete(self, id_: models.CategoryId) -> None:
        ...

    async def get_by_workspace_id(self, workspace_id: models.WorkspaceId) -> list[models.Category]:
        ...

    async def get_by_workspace_id_and_name(
        self,
        workspace_id: models.WorkspaceId,
        name: str,
    ) -> models.Category:
        ...


class CategoriesRepositoryImpl(CategoriesRepository):
    def __init__(self, db_engine: AsyncEngine) -> None:
        self._impl: SQLAlchemyRepository[
            models.Category,
            models.CategoryId,
            models.CategoryCreate,
            models.CategoryUpdate,
        ] = SQLAlchemyRepository(db_engine=db_engine, mapper=_CategoriesMapper())

    async def create(self, create_model: models.CategoryCreate) -> models.Category:
        return await self._impl.create(create_model)

    async def get(self, id_: models.CategoryId) -> models.Category:
        return await self._impl.get(id_)

    async def update(
        self,
        id_: models.CategoryId,
        update_model: models.CategoryUpdate,
    ) -> models.Category:
        return await self._impl.update(id_, update_model)

    async def delete(self, id_: models.CategoryId) -> None:
        return await self._impl.delete(id_)

    async def get_by_workspace_id(self, workspace_id: models.WorkspaceId) -> list[models.Category]:
        query = sa.select(db.Category).where(db.Category.workspace_id == workspace_id)
        return await self._impl.fetch_many(query)

    async def get_by_workspace_id_and_name(
        self,
        workspace_id: models.WorkspaceId,
        name: str,
    ) -> models.Category:
        query = sa.select(db.Category).where(
            sa.and_(
                db.Category.workspace_id == workspace_id,
                db.Category.name == name,
            ),
        )
        return await self._impl.fetch_one(query)
