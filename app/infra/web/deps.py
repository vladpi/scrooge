import rodi
from fastapi import Depends, Request
from fastapi.security import SecurityScopes
from fastapi_login import LoginManager

from app import models


async def get_container(request: Request) -> rodi.Container:
    return request.app.state.container


async def get_login_manager(request: Request) -> LoginManager:
    return request.app.state.login_manager


async def authenticated_user(
    request: Request,
    security_scopes: SecurityScopes = None,
    login_manager: LoginManager = Depends(get_login_manager),
) -> models.User:
    return await login_manager(request, security_scopes)
