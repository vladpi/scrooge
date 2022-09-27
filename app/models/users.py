from typing import Optional

from .base import (
    BaseCreateRequest,
    BaseModel,
    BaseUpdateRequest,
    IntIdentity,
    UUIDIdentity,
)


class UserId(UUIDIdentity):
    """User ID"""


class User(BaseModel):
    id: UserId


class UserCreate(BaseCreateRequest):
    """Create User Request Schema"""


class UserUpdate(BaseUpdateRequest):
    """Update User Request Schema"""


class TelegramUserId(IntIdentity):
    """Telegram User ID"""


class TelegramUser(BaseModel):
    id: TelegramUserId
    user_id: UserId

    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class TelegramUserCreate(BaseCreateRequest):
    id: TelegramUserId
    user_id: UserId

    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class TelegramUserUpdate(BaseUpdateRequest):
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
