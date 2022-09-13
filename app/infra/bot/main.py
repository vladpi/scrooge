import logging

import fastapi

from .events import register_events
from .routes import register_routes

logger = logging.getLogger(__name__)

APP_TITLE = 'scrooge-bot'


def create_app() -> fastapi.FastAPI:
    logger.info(f'Creating {APP_TITLE} app')
    app = fastapi.FastAPI(title=APP_TITLE)

    register_events(app)
    register_routes(app)

    return app
