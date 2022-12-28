import abc
import logging

import databases
import sqlalchemy as sa

from app import db, models

from .base import RepositoryBase
from .sql import DatabasesRepositoryImpl, RelationalMapper

logger = logging.getLogger(__name__)


class _CategoriesMapper(RelationalMapper):
    __model__ = models.Category
    __db_model__ = db.Category


class CategoriesRepository(  # noqa: B024 FIXME
    RepositoryBase[
        models.Category,
        models.CategoryId,
        models.CategoryCreate,
        models.CategoryUpdate,
    ],
    abc.ABC,
):
    """Abstract Categories Repository"""

    async def get_by_workspace_id(self, workspace_id: models.WorkspaceId) -> list[models.Category]:
        raise NotImplementedError

    async def get_by_workspace_id_and_name(
        self,
        workspace_id: models.WorkspaceId,
        name: str,
    ) -> models.Category:
        raise NotImplementedError


class CategoriesRepositoryImpl(CategoriesRepository):
    def __init__(self, db_conn: databases.Database) -> None:
        self._impl: DatabasesRepositoryImpl = DatabasesRepositoryImpl(db_conn, _CategoriesMapper())

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
        query = sa.select([db.Category.__table__]).where(
            db.Category.workspace_id == workspace_id,
        )
        return await self._impl.find_many(query)

    async def get_by_workspace_id_and_name(
        self,
        workspace_id: models.WorkspaceId,
        name: str,
    ) -> models.Category:
        query = sa.select([db.Category.__table__]).where(
            sa.and_(
                db.Category.workspace_id == workspace_id,
                db.Category.name == name,
            ),
        )
        return await self._impl.find_one(query)
