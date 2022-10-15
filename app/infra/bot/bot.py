from typing import Optional

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.types import ParseMode
from pydantic import RedisDsn

from .handlers import HANDLERS
from .middlewares import CtxMiddleware, UserMiddleware, WorkspaceMiddleware


async def create_bot(
    bot_token: str,
    parse_mode: ParseMode = ParseMode.HTML,
    webhook_host: Optional[str] = None,
) -> Bot:
    bot = Bot(token=bot_token, parse_mode=parse_mode)

    if webhook_host is not None:
        url = f'{webhook_host}/bot/{bot_token}'
        current_url = (await bot.get_webhook_info())['url']

        if current_url != url:
            await bot.set_webhook(url=url, drop_pending_updates=True)

    return bot


async def create_dispatcher(bot: Bot, redis_url: Optional[RedisDsn] = None) -> Dispatcher:
    storage = MemoryStorage()

    if redis_url is not None:
        redis_db = None
        if redis_url.path is not None:
            redis_db = int(redis_url.path.replace('/', ''))

        storage = RedisStorage2(
            host=redis_url.host,
            port=redis_url.port,
            password=redis_url.password,
            db=redis_db,
        )

    dispatcher = Dispatcher(bot, storage=storage)
    _setup_dispatcher_middlewares(dispatcher)
    _setup_dispatcher_handlers(dispatcher)

    return dispatcher


def _setup_dispatcher_middlewares(dispatcher: Dispatcher) -> None:
    dispatcher.setup_middleware(CtxMiddleware())
    dispatcher.setup_middleware(UserMiddleware())
    dispatcher.setup_middleware(WorkspaceMiddleware())


def _setup_dispatcher_handlers(dispatcher: Dispatcher) -> None:
    for handlers_module in HANDLERS:
        handlers_module.setup_handlers(dispatcher)
