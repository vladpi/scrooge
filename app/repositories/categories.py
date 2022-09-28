import abc
import logging
from typing import TYPE_CHECKING

from app import db, models

from .base import RepositoryBase
from .sql import DatabasesRepositoryImpl, RelationalMapper

if TYPE_CHECKING:
    from databases import Database

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


class CategoriesRepositoryImpl(CategoriesRepository):
    def __init__(self, db_conn: 'Database') -> None:
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
