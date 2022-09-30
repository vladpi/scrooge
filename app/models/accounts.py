from decimal import Decimal

from .base import BaseCreateRequest, BaseModel, BaseUpdateRequest, UUIDIdentity
from .core import Currency
from .workspaces import WorkspaceId


class AccountId(UUIDIdentity):
    """Account ID"""


class Account(BaseModel):
    id: AccountId
    workspace_id: WorkspaceId

    name: str

    balance: Decimal
    currency: Currency


class AccountCreate(BaseCreateRequest):
    workspace_id: WorkspaceId

    name: str

    balance: Decimal = Decimal('0')
    currency: Currency


class AccountUpdate(BaseUpdateRequest):
    name: str

    balance: Decimal
    currency: Currency
