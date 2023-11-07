from blacksheep import Response
from blacksheep.server.controllers import Controller, get
from guardpost.authentication import Identity


class Home(Controller):
    @get()
    def index(self, user: Identity | None) -> Response:
        # Since the @get() decorator is used without arguments, the URL path
        # is by default "/"

        # Since the view function is called without parameters, the name is
        # obtained from the calling request handler: 'index',
        # -> /views/home/index.html
        return self.view()

    @get(None)
    def example(self) -> Response:
        # Since the @get() decorator is used explicitly with None, the URL path
        # is obtained from the method name: "/example"

        # Since the view function is called without parameters, the name is
        # obtained from the calling request handler: 'example',
        # -> /views/home/example.html
        return self.view()
