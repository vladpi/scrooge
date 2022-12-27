import fastapi
import punq
from fastapi_security_telegram_webhook import OnlyTelegramNetwork

telegram_webhook_security = OnlyTelegramNetwork()


async def get_container(request: fastapi.Request) -> punq.Container:
    return request.app.state.container
