from blacksheep import Application, Request
from guardpost.authentication import AuthenticationHandler, Identity

from app.settings import Settings


class ExampleAuthHandler(AuthenticationHandler):
    def __init__(self) -> None:
        pass

    async def authenticate(self, context: Request) -> Identity | None:
        # TODO: apply the desired logic to obtain a user's identity from
        # information in the web request, for example reading a piece of
        # information from a header (or cookie).
        header_value = context.get_first_header(b"Authorization")

        if header_value:
            # implement your logic to obtain the user
            # in this example, an identity is hard-coded just to illustrate
            # testing in the next paragraph
            context.identity = Identity({"name": "Jan Kowalski"}, "MOCK")
        else:
            # if the request cannot be authenticated, set the context.identity
            # to None - do not throw exception because the app might support
            # different ways to authenticate users
            context.identity = None
        return context.identity


def configure_authentication(app: Application, settings: Settings) -> None:
    """
    Configure authentication as desired. For reference:
    https://www.neoteroi.dev/blacksheep/authentication/
    """

    app.use_authentication().add(ExampleAuthHandler())
