from app import models, repositories
from app.domains import (
    CreateUserDefaultCategoriesRequest,
    create_user_default_categories,
)

from .schemas import CreateWorkspaceRequest


async def create_workspace(
    workspaces_repo: repositories.WorkspacesRepository,
    categories_repo: repositories.CategoriesRepository,
    request: CreateWorkspaceRequest,
) -> models.Workspace:
    workspace = await workspaces_repo.create(
        models.WorkspaceCreate(owner_id=request.owner_id),
    )

    if request.init_defaults:
        await create_user_default_categories(
            categories_repo,
            CreateUserDefaultCategoriesRequest(workspace_id=workspace.id),
        )

    return workspace
