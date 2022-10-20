from typing import List

from app import models, repositories

from .consts import DEFAULT_CATEGORIES
from .schemas import CreateUserDefaultCategoriesRequest, CreateWorkspaceCategory


async def create_user_default_categories(
    categories_repo: repositories.CategoriesRepository,
    request: CreateUserDefaultCategoriesRequest,
) -> List[models.Category]:
    categories = []

    for default_category in DEFAULT_CATEGORIES:
        category = await categories_repo.create(
            models.CategoryCreate(
                workspace_id=request.workspace_id,
                name=default_category.name,
                is_income=default_category.is_income,
                is_outcome=default_category.is_outcome,
            ),
        )
        categories.append(category)

    return categories


async def create_workspace_category(
    repos: repositories.Repositories,
    request: CreateWorkspaceCategory,
) -> models.Category:
    return await repos.categories_repo.create(
        models.CategoryCreate(
            workspace_id=request.workspace_id,
            name=request.name,
            is_income=request.is_income,
            is_outcome=request.is_outcome,
        ),
    )


async def get_workspace_categories(
    repos: repositories.Repositories,
    workspace_id: models.WorkspaceId,
) -> List[models.Category]:
    return await repos.categories_repo.get_by_workspace_id(workspace_id)


async def get_workspace_category_by_name(
    repos: repositories.Repositories,
    workspace_id: models.WorkspaceId,
    name: str,
) -> models.Category:
    return await repos.categories_repo.get_by_workspace_id_and_name(workspace_id, name)
