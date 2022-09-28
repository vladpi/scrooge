from pydantic import BaseModel

from app import models


class CreateUserDefaultCategoriesRequest(BaseModel):
    workspace_id: models.WorkspaceId
