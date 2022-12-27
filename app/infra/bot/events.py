import logging
from typing import Callable

import databases
import fastapi

logger = logging.getLogger(__name__)


def register_events(app: fastapi.FastAPI) -> None:
    logger.info(f'Registering events for {app.title}')
    app.router.on_startup = [_on_startup(app)]
    app.router.on_shutdown = [_on_shutdown(app)]


def _on_startup(app: fastapi.FastAPI) -> Callable:
    async def startup_handler() -> None:  # noqa: WPS430
        logger.info(f'Starting app {app.title}')

        db = app.state.container.resolve(databases.Database)
        await db.connect()

        await app.state.bot.setup()

    return startup_handler


def _on_shutdown(app: fastapi.FastAPI) -> Callable:
    async def shutdown_handler() -> None:  # noqa: WPS430
        logger.info(f'Shutting down app {app.title}')

        try:
            await app.state.bot.shutdown()

            db = app.state.container.resolve(databases.Database)
            await db.disconnect()

        except Exception:
            logger.exception(f'Context of {app.title} is not properly configured, failed to close')

    return shutdown_handler
