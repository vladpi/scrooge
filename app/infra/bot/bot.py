import logging

import aiogram
import punq
from aiogram.fsm.storage.base import BaseStorage
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import BotCommand
from redis.asyncio.client import Redis

from app.settings import BotSettings

from .handlers import HANDLERS
from .middlewares import CtxMiddleware, UserMiddleware, WorkspaceMiddleware

logger = logging.getLogger(__name__)


class Bot(aiogram.Bot):
    def __init__(self, settings: BotSettings) -> None:
        super().__init__(
            token=settings.TOKEN.get_secret_value(),
            parse_mode='HTML',  # FIXME
        )
        self._webhook_host = settings.WEBHOOK_HOST

    async def setup(self) -> None:
        bot_info = await self.get_me()
        logger.info('Setup bot %s', bot_info.username)

        if self._webhook_host is not None:
            url = f'{self._webhook_host}/bot/{self.token}'
            webhook_info = await self.get_webhook_info()

            if webhook_info.url != url:
                await self.set_webhook(url=url)

        await self.set_my_commands(
            commands=[
                BotCommand(command='outcome', description='Добавить расход'),
                BotCommand(command='income', description='Добавить доход'),
            ],
        )

    async def shutdown(self) -> None:
        await self.session.close()


class Dispatcher(aiogram.Dispatcher):
    def __init__(
        self,
        bot: aiogram.Bot,
        settings: BotSettings,
        container: punq.Container,
    ) -> None:
        storage: BaseStorage = MemoryStorage()

        if settings.REDIS_URL is not None:
            redis_db = 0
            if settings.REDIS_URL.path is not None:
                redis_db = int(settings.REDIS_URL.path.replace('/', ''))

            storage = RedisStorage(
                Redis(
                    host=settings.REDIS_URL.host,  # type: ignore
                    port=int(settings.REDIS_URL.port),  # type: ignore
                    password=settings.REDIS_URL.password,
                    db=redis_db,
                ),
            )

        super().__init__(
            bot=bot,
            storage=storage,
        )

        self.update.outer_middleware(CtxMiddleware(container))
        self.update.outer_middleware(UserMiddleware(container))
        self.update.outer_middleware(WorkspaceMiddleware(container))

        for handlers_module in HANDLERS:
            handlers_module.setup_handlers(self)
