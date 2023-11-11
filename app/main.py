"""
This module configures the BlackSheep application before it starts.
"""
from blacksheep import Application
from blacksheepsqlalchemy import use_sqlalchemy
from rodi import Container

from app.auth import configure_authentication
from app.errors import configure_error_handlers
from app.services import configure_services
from app.settings import Settings, load_settings
from app.templating import configure_templating


def configure_application(
    services: Container,
    settings: Settings,
) -> Application:
    app = Application(services=services, show_error_details=settings.app.show_error_details)

    app.serve_files("app/static")
    configure_authentication(app, settings)
    configure_templating(app, settings)
    configure_error_handlers(app)

    use_sqlalchemy(app, connection_string=settings.db.connection_url)

    return app


app = configure_application(*configure_services(load_settings()))
