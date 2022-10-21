from app import models, repositories

from .consts import DEFAULT_CATEGORIES
from .schemas import CreateUserDefaultCategoriesRequest, CreateWorkspaceCategory


class CategoriesService:  # noqa: WPS306
    def __init__(self, categories_repo: repositories.CategoriesRepository) -> None:
        self._repo = categories_repo

    async def create_user_default_categories(
        self,
        request: CreateUserDefaultCategoriesRequest,
    ) -> list[models.Category]:
        categories = []

        for default_category in DEFAULT_CATEGORIES:
            category = await self._repo.create(
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
        self,
        request: CreateWorkspaceCategory,
    ) -> models.Category:
        return await self._repo.create(
            models.CategoryCreate(
                workspace_id=request.workspace_id,
                name=request.name,
                is_income=request.is_income,
                is_outcome=request.is_outcome,
            ),
        )

    async def get_workspace_categories(
        self,
        workspace_id: models.WorkspaceId,
    ) -> list[models.Category]:
        return await self._repo.get_by_workspace_id(workspace_id)

    async def get_workspace_category_by_name(
        self,
        workspace_id: models.WorkspaceId,
        name: str,
    ) -> models.Category:
        return await self._repo.get_by_workspace_id_and_name(workspace_id, name)
