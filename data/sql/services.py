from rodi import Container

from domain.users import UsersRepository

from .users import SQLUsersRepository


def register_sql_services(container: Container) -> None:
    container.add_scoped(UsersRepository, SQLUsersRepository)
