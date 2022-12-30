from pydantic import BaseModel

from app import models


class CreateOrUpdateTelegramUserRequest(BaseModel):
    telegram_user_id: models.TelegramUserId

    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None

    avatar_url: str | None = None
