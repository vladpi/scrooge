from app import models, repositories
from app.domains import (
    AccountsService,
    CategoriesService,
    CreateUserDefaultAccounts,
    CreateUserDefaultCategoriesRequest,
)

from .schemas import CreateWorkspaceRequest


class WorkspacesService:  # noqa: WPS306
    def __init__(
        self,
        workspaces_repo: repositories.WorkspacesRepository,
        accounts_service: AccountsService,
        categorires_service: CategoriesService,
    ) -> None:
        self._repo = workspaces_repo
        self._accounts_srv = accounts_service
        self._categorires_srv = categorires_service

    async def create_workspace(
        self,
        request: CreateWorkspaceRequest,
    ) -> models.Workspace:
        workspace = await self._repo.create(
            models.WorkspaceCreate(owner_id=request.owner_id),
        )

        if request.init_defaults:
            await self._categorires_srv.create_user_default_categories(
                CreateUserDefaultCategoriesRequest(workspace_id=workspace.id),
            )
            await self._accounts_srv.create_user_defaults_accounts(
                CreateUserDefaultAccounts(workspace_id=workspace.id),
            )

        return workspace

    async def get_user_workspace(
        self,
        user_id: models.UserId,
    ) -> models.Workspace:
        return await self._repo.get_by_owner_id(user_id)
