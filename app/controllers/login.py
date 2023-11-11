from dataclasses import dataclass

from blacksheep import FromForm, Response
from blacksheep.server.authentication.cookie import CookieAuthentication
from blacksheep.server.controllers import Controller, get, post

from domain.users import UsersService


@dataclass
class LoginUserForm:
    email: str
    password: str


class Login(Controller):
    def __init__(self, users_service: UsersService, auth_handler: CookieAuthentication) -> None:
        super().__init__()
        self.users_service = users_service
        self.auth_handler = auth_handler

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

    @post()
    async def login_user(self, data: FromForm[LoginUserForm]) -> Response:
        user = await self.users_service.authenticate_user_by_email(
            data.value.email, data.value.password
        )

        response = self.redirect("/")
        self.auth_handler.set_cookie({"id": str(user.id)}, response)

        return response
