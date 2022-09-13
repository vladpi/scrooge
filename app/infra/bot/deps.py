import fastapi
from fastapi_security_telegram_webhook import OnlyTelegramNetwork

from . import context

telegram_webhook_security = OnlyTelegramNetwork()


async def get_context(request: fastapi.Request) -> context.Context:
    return request.app.state.context
