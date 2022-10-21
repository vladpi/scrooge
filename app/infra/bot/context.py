import logging

import aiogram
import databases
import pydantic

from app import domains, repositories, settings
from libs.context import ContextBase

from .bot import create_bot, create_dispatcher

logger = logging.getLogger(__name__)


class Services(pydantic.BaseModel):
    users: domains.UsersService
    accounts: domains.AccountsService
    categories: domains.CategoriesService
    transactions: domains.TransactionsService
    workspaces: domains.WorkspacesService

    class Config:  # noqa: WPS306, WPS431
        arbitrary_types_allowed = True
        allow_mutation = False


class Context(ContextBase):
    app_settings: settings.AppSettings
    bot_settings: settings.BotSettings

    bot: aiogram.Bot
    dispatcher: aiogram.Dispatcher

    db: databases.Database

    repos: repositories.Repositories
    services: Services

    async def _do_close(self) -> None:
        bot_sesion = await self.bot.get_session()
        if bot_sesion is not None:
            await bot_sesion.close()
        else:
            logger.info('Telegram bot session already closed')

        await self.db.disconnect()


async def make_context() -> Context:
    try:
        return await _make_context()

    except Exception:
        logger.exception('Failed to initialize bot context')
        raise


async def _make_context() -> Context:  # noqa: WPS210
    logger.info('Initializing bot context')

    app_settings = settings.AppSettings()
    db = databases.Database(app_settings.DATABASE_URL)
    await db.connect()

    bot_settings = settings.BotSettings()
    bot = await create_bot(
        bot_token=bot_settings.TOKEN.get_secret_value(),
        webhook_host=bot_settings.WEBHOOK_HOST,
    )
    dispatcher = await create_dispatcher(bot, bot_settings.REDIS_URL)

    repos = _make_repos(db)
    services = _make_services(repos)

    context = Context(
        app_settings=app_settings,
        bot_settings=bot_settings,
        bot=bot,
        dispatcher=dispatcher,
        db=db,
        repos=repos,
        services=services,
    )

    # bad hack :(
    bot.data['ctx'] = context

    logger.info('Bot context successfully initialized')

    return context


def _make_repos(db: databases.Database) -> repositories.Repositories:
    return repositories.Repositories(
        users_repo=repositories.UsersRepositoryImpl(db),
        telegram_users_repo=repositories.TelegramUsersRepositoryImpl(db),
        workspaces_repo=repositories.WorkspacesRepositoryImpl(db),
        categories_repo=repositories.CategoriesRepositoryImpl(db),
        accounts_repo=repositories.AccountsRepositoryImpl(db),
        transactions_repo=repositories.TransactionsRepositoryImpl(db),
    )


def _make_services(repos: repositories.Repositories) -> Services:
    users_srv = domains.UsersService(repos.users_repo, repos.telegram_users_repo)
    accounts_srv = domains.AccountsService(repos.accounts_repo)
    categories_srv = domains.CategoriesService(repos.categories_repo)
    transactions_srv = domains.TransactionsService(repos.transactions_repo, repos.accounts_repo)
    workspaces_srv = domains.WorkspacesService(repos.workspaces_repo, accounts_srv, categories_srv)

    return Services(
        users=users_srv,
        accounts=accounts_srv,
        categories=categories_srv,
        transactions=transactions_srv,
        workspaces=workspaces_srv,
    )
