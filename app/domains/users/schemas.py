from typing import Optional

from pydantic import BaseModel

from app import models


class CreateOrUpdateTelegramUserRequest(BaseModel):
    telegram_user_id: models.TelegramUserId

    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
