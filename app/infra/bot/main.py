import logging

import fastapi
import punq

from app.settings import BotSettings

from .bot import Bot, Dispatcher
from .events import register_events
from .routes import register_routes

logger = logging.getLogger(__name__)

APP_TITLE = 'scrooge-bot'


def create_app(container: punq.Container) -> fastapi.FastAPI:
    logger.info(f'Creating {APP_TITLE} app')
    app = fastapi.FastAPI(title=APP_TITLE)

    app.state.container = container

    bot_settings = container.resolve(BotSettings)
    bot = Bot(bot_settings)
    dispatcher = Dispatcher(bot, bot_settings, container)

    app.state.bot = bot
    app.state.dispatcher = dispatcher

    register_events(app)
    register_routes(app)

    return app
