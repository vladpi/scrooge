from blacksheep import Response
from blacksheep.server.controllers import Controller, get


class Login(Controller):
    @classmethod
    def route(cls) -> str | None:
        return "login"

    @get()
    def index(self) -> Response:
        # Since the @get() decorator is used without arguments, the URL path
        # is by default "/"

        # Since the view function is called without parameters, the name is
        # obtained from the calling request handler: 'index',
        # -> /views/home/index.html
        return self.view()
