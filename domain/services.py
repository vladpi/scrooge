from rodi import Container

from .passwords import PasswordsService
from .users import UsersService


def register_services(container: Container) -> None:
    container.add_scoped(UsersService)
    container.add_scoped(PasswordsService)
