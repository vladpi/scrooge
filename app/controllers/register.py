from blacksheep import FromForm, Response
from blacksheep.server.authentication.cookie import CookieAuthentication
from blacksheep.server.authorization import allow_anonymous
from blacksheep.server.controllers import Controller, get, post

from domain.users import CreateUserInput, UsersService


class Register(Controller):
    def __init__(self, users_service: UsersService, auth_handler: CookieAuthentication) -> None:
        super().__init__()
        self.users_service = users_service
        self.auth_handler = auth_handler

    @classmethod
    def route(cls) -> str | None:
        return "register"

    @allow_anonymous()
    @get()
    def index(self) -> Response:
        # Since the @get() decorator is used without arguments, the URL path
        # is by default "/"

        # Since the view function is called without parameters, the name is
        # obtained from the calling request handler: 'index',
        # -> /views/home/index.html
        return self.view()

    @allow_anonymous()
    @post()
    async def register_user(self, data: FromForm[CreateUserInput]) -> Response:
        user = await self.users_service.create_user(data.value)

        response = self.redirect("/")
        self.auth_handler.set_cookie({"id": str(user.id), "foo": "bar"}, response)

        return response
