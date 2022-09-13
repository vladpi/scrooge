import logging

import aiogram
import databases

from app import settings
from libs.context import ContextBase

from .bot import create_bot, create_dispatcher

logger = logging.getLogger(__name__)


class Context(ContextBase):
    app_settings: settings.AppSettings
    bot_settings: settings.BotSettings

    bot: aiogram.Bot
    dispatcher: aiogram.Dispatcher

    db: databases.Database

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

    context = Context(
        app_settings=app_settings,
        bot_settings=bot_settings,
        bot=bot,
        dispatcher=dispatcher,
        db=db,
    )

    # bad hack :(
    bot.data['ctx'] = context

    logger.info('Bot context successfully initialized')

    return context
