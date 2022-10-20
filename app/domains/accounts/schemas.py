from pydantic import BaseModel

from app import models


class CreateUserDefaultAccounts(BaseModel):
    workspace_id: models.WorkspaceId
    currency: models.Currency = models.Currency.RUB


class CreateWorkspaceAccount(BaseModel):
    workspace_id: models.WorkspaceId
    name: str
    currency: models.Currency = models.Currency.RUB
