from typing import Any, Dict

from aiogram import Bot, Dispatcher
from aiogram.types import Update
from fastapi import APIRouter, Body, Depends, FastAPI
from fastapi_security_telegram_webhook import OnlyTelegramNetwork
from starlette import status
from starlette.responses import Response

from .context import Context
from .deps import get_context, telegram_webhook_security

router = APIRouter(prefix='/bot')


def register_routes(app: FastAPI) -> None:
    app.include_router(router)


@router.post('/{secret:str}', include_in_schema=False)
async def handle_webhook(
    secret: str,
    raw_update: Dict[str, Any] = Body(...),
    ctx: Context = Depends(get_context),
    security: OnlyTelegramNetwork = Depends(telegram_webhook_security),
) -> Response:
    Bot.set_current(ctx.bot)
    Dispatcher.set_current(ctx.dispatcher)
    await ctx.dispatcher.process_update(Update(**raw_update))
    return Response(status_code=status.HTTP_200_OK)
