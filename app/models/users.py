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

    first_name: str | None = None
    last_name: str | None = None

    avatar_url: str | None = None

    @property
    def full_name(self) -> str:
        return ' '.join(filter(None, [self.first_name, self.last_name]))


class UserCreate(BaseCreateRequest):
    """Create User Request Schema"""

    first_name: str | None = None
    last_name: str | None = None

    avatar_url: str | None = None


class UserUpdate(BaseUpdateRequest):
    """Update User Request Schema"""

    first_name: str | None = None
    last_name: str | None = None

    avatar_url: str | None = None


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
