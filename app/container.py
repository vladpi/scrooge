import databases
from neoteroi import di

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


def get_container() -> di.Container:  # noqa: WPS210
    container = di.Container()

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
        databases.Database,
        instance=databases.Database(url=app_settings.DATABASE_URL),
    )

    for interface, implementation in REPOS:
        container.register(interface, implementation)

    for service in SERVICES:
        container.register(service)

    return container
