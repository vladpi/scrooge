import databases
import punq

from app import domains, repositories, settings

REPOS = (
    (repositories.UsersRepository, repositories.UsersRepositoryImpl),
    (repositories.TelegramUsersRepository, repositories.TelegramUsersRepositoryImpl),
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


def get_container() -> punq.Container:  # noqa: WPS210
    container = punq.Container()

    app_settings = settings.AppSettings()
    bot_settings = settings.BotSettings()

    container.register(
        settings.AppSettings,
        instance=app_settings,
        scope=punq.Scope.singleton,
    )
    container.register(
        settings.BotSettings,
        instance=bot_settings,
        scope=punq.Scope.singleton,
    )

    container.register(
        databases.Database,
        instance=databases.Database(url=app_settings.DATABASE_URL),
        scope=punq.Scope.singleton,
    )

    for interface, implementation in REPOS:
        container.register(interface, implementation)

    for service in SERVICES:
        container.register(service, service)

    return container
