import rodi
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from app import domains, repositories, settings

REPOS = (
    (repositories.UsersRepository, repositories.UsersRepositoryImpl),
    (repositories.TelegramUsersRepository, repositories.TelegramUsersRepositoryImpl),
    (repositories.WorkspacesRepository, repositories.WorkspacesRepositoryImpl),
    (repositories.CategoriesRepository, repositories.CategoriesRepositoryImpl),
    (repositories.AccountsRepository, repositories.AccountsRepositoryImpl),
    (repositories.TranasactionssRepository, repositories.TransactionsRepositoryImpl),
)


SERVICES = (
    domains.UsersService,
    domains.AccountsService,
    domains.CategoriesService,
    domains.TransactionsService,
    domains.WorkspacesService,
)


def get_container() -> rodi.Container:  # noqa: WPS210
    container = rodi.Container()

    app_settings = settings.AppSettings()
    bot_settings = settings.BotSettings()

    container.register(
        settings.AppSettings,
        instance=app_settings,
    )
    container.register(
        settings.BotSettings,
        instance=bot_settings,
    )

    container.register(
        AsyncEngine,
        instance=create_async_engine(url=app_settings.DATABASE_URL),
    )

    for interface, implementation in REPOS:
        container.register(interface, implementation)

    for service in SERVICES:
        container.register(service)

    return container
