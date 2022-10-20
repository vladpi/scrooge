from pydantic import BaseModel

from app import models


class CreateUserDefaultCategoriesRequest(BaseModel):
    workspace_id: models.WorkspaceId


class CreateWorkspaceCategory(BaseModel):
    workspace_id: models.WorkspaceId
    name: str
    is_income: bool = True
    is_outcome: bool = True
