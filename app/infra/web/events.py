import logging
from typing import Callable

import fastapi

logger = logging.getLogger(__name__)


def register_events(app: fastapi.FastAPI) -> None:
    logger.info(f'Registering events for {app.title}')
    app.router.on_startup = [_on_startup(app)]
    app.router.on_shutdown = [_on_shutdown(app)]


def _on_startup(app: fastapi.FastAPI) -> Callable:
    async def startup_handler() -> None:  # noqa: WPS430
        logger.info(f'Starting app {app.title}')

    return startup_handler


def _on_shutdown(app: fastapi.FastAPI) -> Callable:
    async def shutdown_handler() -> None:  # noqa: WPS430
        logger.info(f'Shutting down app {app.title}')

    return shutdown_handler
