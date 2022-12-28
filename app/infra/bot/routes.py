from typing import Any, Dict

from aiogram.types import Update
from fastapi import APIRouter, Body, Depends, FastAPI, Request
from fastapi_security_telegram_webhook import OnlyTelegramNetwork
from neoteroi import di
from starlette import status
from starlette.responses import Response

from .deps import get_container, telegram_webhook_security

router = APIRouter(prefix='/bot')


def register_routes(app: FastAPI) -> None:
    app.include_router(router)


@router.post('/{secret:str}', include_in_schema=False)
async def handle_webhook(
    request: Request,
    secret: str,
    raw_update: Dict[str, Any] = Body(...),
    container: di.Container = Depends(get_container),
    security: OnlyTelegramNetwork = Depends(telegram_webhook_security),
) -> Response:

    bot = request.app.state.bot
    dispatcher = request.app.state.dispatcher

    await dispatcher.feed_webhook_update(bot, Update(**raw_update))

    return Response(status_code=status.HTTP_200_OK)
