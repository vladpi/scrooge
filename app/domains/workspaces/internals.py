from app import models, repositories
from app.domains import (
    CreateUserDefaultAccounts,
    CreateUserDefaultCategoriesRequest,
    create_user_default_categories,
    create_user_defaults_accounts,
)

from .schemas import CreateWorkspaceRequest


async def create_workspace(
    repos: repositories.Repositories,
    request: CreateWorkspaceRequest,
) -> models.Workspace:
    workspace = await repos.workspaces_repo.create(
        models.WorkspaceCreate(owner_id=request.owner_id),
    )

    if request.init_defaults:
        await create_user_default_categories(
            repos.categories_repo,
            CreateUserDefaultCategoriesRequest(workspace_id=workspace.id),
        )
        await create_user_defaults_accounts(
            repos.accounts_repo,
            CreateUserDefaultAccounts(workspace_id=workspace.id),
        )

    return workspace
