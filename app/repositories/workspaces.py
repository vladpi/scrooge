import abc
import logging
from typing import TYPE_CHECKING

from app import db, models

from .base import RepositoryBase
from .sql import DatabasesRepositoryImpl, RelationalMapper

if TYPE_CHECKING:
    from databases import Database

logger = logging.getLogger(__name__)


class _WorkspacesMapper(RelationalMapper):
    __model__ = models.Workspace
    __db_model__ = db.Workspace


class WorkspacesRepository(  # noqa: B024 FIXME
    RepositoryBase[
        models.Workspace,
        models.WorkspaceId,
        models.WorkspaceCreate,
        models.WorkspaceUpdate,
    ],
    abc.ABC,
):
    """Abstract Workspaces Repository"""


class WorkspacesRepositoryImpl(WorkspacesRepository):
    def __init__(self, db_conn: 'Database') -> None:
        self._impl: DatabasesRepositoryImpl = DatabasesRepositoryImpl(db_conn, _WorkspacesMapper())

    async def create(self, create_model: models.WorkspaceCreate) -> models.Workspace:
        return await self._impl.create(create_model)

    async def get(self, id_: models.WorkspaceId) -> models.Workspace:
        return await self._impl.get(id_)

    async def update(
        self,
        id_: models.WorkspaceId,
        update_model: models.WorkspaceUpdate,
    ) -> models.Workspace:
        return await self._impl.update(id_, update_model)

    async def delete(self, id_: models.WorkspaceId) -> None:
        return await self._impl.delete(id_)
