from blacksheep import Response
from blacksheep.server.controllers import Controller, get
from guardpost.authentication import Identity

from domain.users import UsersService


class Home(Controller):
    def __init__(self, users_service: UsersService) -> None:
        super().__init__()
        self.users_service = users_service

    @get()
    async def index(self, identity: Identity) -> Response:
        user = await self.users_service.get_user(identity.get("id"))
        # Since the @get() decorator is used without arguments, the URL path
        # is by default "/"

        # Since the view function is called without parameters, the name is
        # obtained from the calling request handler: 'index',
        # -> /views/home/index.html
        return self.view(model={"user": user})
