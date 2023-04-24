import logging
from datetime import timedelta

import rodi
from fastapi import APIRouter, Depends, FastAPI, Request, status
from fastapi.responses import RedirectResponse, Response
from fastapi.templating import Jinja2Templates
from fastapi_login import LoginManager

from app import domains, models
from app.domains.users.schemas import CreateOrUpdateTelegramUserRequest
from app.infra.web import deps

from .schemas import TelegramLoginCallbackRequestSchema

router = APIRouter(include_in_schema=False)
templates = Jinja2Templates('app/templates/web')

logger = logging.getLogger(__name__)


def register_routes(app: FastAPI) -> None:
    app.include_router(router)


@router.get('/')
async def index(
    request: Request,
    user: models.User = Depends(deps.authenticated_user),
) -> Response:
    return templates.TemplateResponse('index.html', context={'request': request, 'user': user})


@router.get('/login')
async def get_login_page(
    request: Request,
    user: models.User | None = Depends(deps.maybe_authenticated_user),
) -> Response:
    if user is not None:
        return RedirectResponse('/', status_code=status.HTTP_302_FOUND)

    return templates.TemplateResponse('login.html', context={'request': request})


@router.get('/tg-callback')
async def handle_tg_login_callback(
    request: Request,
    callback_data: TelegramLoginCallbackRequestSchema = Depends(),
    container: rodi.Container = Depends(deps.get_container),
    login_manager: LoginManager = Depends(deps.get_login_manager),
) -> Response:
    logger.debug(request.query_params)
    logger.debug(callback_data)

    # TODO проверить хэш запроса

    users_service = container.resolve(domains.UsersService)

    tg_user = await users_service.create_or_update_user_from_telegram(
        CreateOrUpdateTelegramUserRequest(
            telegram_user_id=callback_data.id,
            username=callback_data.username,
            first_name=callback_data.first_name,
            last_name=callback_data.last_name,
            avatar_url=callback_data.photo_url,
        ),
    )

    response = RedirectResponse('/', status_code=status.HTTP_302_FOUND)

    access_token = login_manager.create_access_token(
        data={'sub': str(tg_user.user_id)},
        expires=timedelta(days=1),
    )
    login_manager.set_cookie(response, access_token)

    return response
