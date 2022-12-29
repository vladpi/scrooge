from typing import Any, Optional

import fastapi_login

from app import models, repositories, settings

LOGIN_PATH = '/login'


class LoginManager(fastapi_login.LoginManager):
    def __init__(
        self,
        app_settings: settings.AppSettings,
        users_repo: repositories.UsersRepository,
    ) -> None:
        super().__init__(
            app_settings.SECRET_KEY.get_secret_value(),
            token_url=LOGIN_PATH,
            use_cookie=True,
        )
        self._users_repo = users_repo

    async def _load_user(self, identifier: Any) -> Optional[models.User]:
        try:
            return await self._users_repo.get(identifier)
        except repositories.NotFoundError:
            return None
