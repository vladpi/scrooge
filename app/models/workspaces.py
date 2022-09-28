from .base import BaseCreateRequest, BaseModel, BaseUpdateRequest, UUIDIdentity
from .users import UserId


class WorkspaceId(UUIDIdentity):
    """Workspace ID"""


class Workspace(BaseModel):
    id: WorkspaceId
    owner_id: UserId


class WorkspaceCreate(BaseCreateRequest):
    owner_id: UserId


class WorkspaceUpdate(BaseUpdateRequest):
    """Update Workspace Request Schema"""
