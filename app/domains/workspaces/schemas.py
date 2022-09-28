from pydantic import BaseModel

from app import models


class CreateWorkspaceRequest(BaseModel):
    owner_id: models.UserId
    init_defaults: bool = False
