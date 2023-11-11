from blacksheep import Application
from blacksheep.server.authentication.cookie import CookieAuthentication
from blacksheep.server.authorization import Policy
from guardpost.common import AuthenticatedRequirement

from app.settings import Settings
from domain.common import Authenticated


def configure_authentication(app: Application, settings: Settings) -> None:
    """
    Configure authentication as desired. For reference:
    https://www.neoteroi.dev/blacksheep/authentication/
    """

    auth_handler = CookieAuthentication()  # TODO add explicit read secret keys from settings
    app.services.add_instance(auth_handler)
    app.use_authentication().add(auth_handler)

    authorization = app.use_authorization()
    authorization.default_policy = Policy(Authenticated, AuthenticatedRequirement())
