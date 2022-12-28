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

    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None


class TelegramUserCreate(BaseCreateRequest):
    id: TelegramUserId
    user_id: UserId

    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None


class TelegramUserUpdate(BaseUpdateRequest):
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
