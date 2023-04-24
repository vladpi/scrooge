import logging

import fastapi
import rodi
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette_wtf import CSRFProtectMiddleware

from app import repositories, settings

from .error_handlers import register_error_handlers
from .events import register_events
from .routes import register_routes
from .security import LoginManager

logger = logging.getLogger(__name__)

APP_TITLE = 'scrooge-web'
SETTINGS = settings.AppSettings()


def create_app(container: rodi.Container) -> fastapi.FastAPI:
    logger.info(f'Creating {APP_TITLE} app')
    app = fastapi.FastAPI(
        title=APP_TITLE,
        docs_url=None,
        middleware=[
            Middleware(SessionMiddleware, secret_key=SETTINGS.SECRET_KEY.get_secret_value()),
            Middleware(CSRFProtectMiddleware, csrf_secret=SETTINGS.SECRET_KEY.get_secret_value()),
        ],
    )

    app.state.container = container

    app_settings = container.resolve(settings.AppSettings)
    users_repo = container.resolve(repositories.UsersRepository)

    app.state.login_manager = LoginManager(app_settings, users_repo)

    register_events(app)
    register_routes(app)
    register_error_handlers(app)

    return app
