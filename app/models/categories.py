from .base import BaseCreateRequest, BaseModel, BaseUpdateRequest, UUIDIdentity
from .workspaces import WorkspaceId


class CategoryId(UUIDIdentity):
    """Category ID"""


class Category(BaseModel):
    id: CategoryId
    workspace_id: WorkspaceId

    name: str

    is_income: bool
    is_outcome: bool


class CategoryCreate(BaseCreateRequest):
    workspace_id: WorkspaceId
    name: str
    is_income: bool
    is_outcome: bool


class CategoryUpdate(BaseUpdateRequest):
    name: str
    is_income: bool
    is_outcome: bool
