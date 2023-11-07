from blacksheep import Application
from blacksheep.server.authentication.cookie import CookieAuthentication

from app.settings import Settings


def configure_authentication(app: Application, settings: Settings) -> None:
    """
    Configure authentication as desired. For reference:
    https://www.neoteroi.dev/blacksheep/authentication/
    """

    auth_handler = CookieAuthentication()  # TODO add explicit read secret keys from settings
    app.services.add_instance(auth_handler)
    app.use_authentication().add(auth_handler)
