import fastapi
from fastapi_security_telegram_webhook import OnlyTelegramNetwork
from neoteroi import di

telegram_webhook_security = OnlyTelegramNetwork()


async def get_container(request: fastapi.Request) -> di.Container:
    return request.app.state.container
