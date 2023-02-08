import fastapi
import rodi
from fastapi_security_telegram_webhook import OnlyTelegramNetwork

telegram_webhook_security = OnlyTelegramNetwork()


async def get_container(request: fastapi.Request) -> rodi.Container:
    return request.app.state.container
