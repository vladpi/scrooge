from typing import TYPE_CHECKING

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext, filters

if TYPE_CHECKING:
    from app.infra.bot.context import Context
    from app.models import TelegramUser


def setup_handlers(dispatcher: Dispatcher) -> None:
    dispatcher.register_message_handler(
        start,
        filters.CommandStart(),
        state='*',
    )


async def start(
    message: types.Message,
    state: FSMContext,
    ctx: 'Context',
    user: 'TelegramUser',
) -> None:
    await message.answer(f'Hello, {user.first_name}!')
