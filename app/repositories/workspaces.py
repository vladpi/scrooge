import logging
from typing import Protocol

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncEngine

from app import db, models

from .sql import RelationalMapper, SQLAlchemyRepository

logger = logging.getLogger(__name__)


class _WorkspacesMapper(RelationalMapper):
    __model__ = models.Workspace
    __db_model__ = db.Workspace


class WorkspacesRepository(Protocol):
    async def create(self, create_model: models.WorkspaceCreate) -> models.Workspace:
        ...

    async def get(self, id_: models.WorkspaceId) -> models.Workspace:
        ...

    async def update(
        self,
        id_: models.WorkspaceId,
        update_model: models.WorkspaceUpdate,
    ) -> models.Workspace:
        ...

    async def delete(self, id_: models.WorkspaceId) -> None:
        ...

    async def get_by_owner_id(self, owner_id: models.UserId) -> models.Workspace:
        ...


class WorkspacesRepositoryImpl(WorkspacesRepository):
    def __init__(self, db_engine: AsyncEngine) -> None:
        self._impl: SQLAlchemyRepository[
            models.Workspace,
            models.WorkspaceId,
            models.WorkspaceCreate,
            models.WorkspaceUpdate,
        ] = SQLAlchemyRepository(db_engine=db_engine, mapper=_WorkspacesMapper())

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

    async def get_by_owner_id(self, owner_id: models.UserId) -> models.Workspace:
        query = sa.select(db.Workspace).where(db.Workspace.owner_id == owner_id)
        return await self._impl.fetch_one(query)
