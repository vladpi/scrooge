from typing import List

from app import models, repositories

from .consts import DEFAULT_CATEGORIES
from .schemas import CreateUserDefaultCategoriesRequest


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
