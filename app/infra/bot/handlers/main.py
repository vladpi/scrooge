from typing import TYPE_CHECKING

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext, filters

if TYPE_CHECKING:
    from app.infra.bot.context import Context


def setup_handlers(dispatcher: Dispatcher) -> None:
    dispatcher.register_message_handler(
        start,
        filters.CommandStart(),
        state='*',
    )


async def start(message: types.Message, state: FSMContext, ctx: 'Context') -> None:
    await message.answer('Hello, world!')
