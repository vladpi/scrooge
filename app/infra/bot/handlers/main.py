from typing import TYPE_CHECKING

import punq
from aiogram import Dispatcher, filters, types
from aiogram.fsm.context import FSMContext

if TYPE_CHECKING:
    from app.models import TelegramUser


def setup_handlers(dispatcher: Dispatcher) -> None:
    dispatcher.message.register(
        start,
        filters.CommandStart(),
    )


async def start(
    message: types.Message,
    state: FSMContext,
    container: punq.Container,
    user: 'TelegramUser',
) -> None:
    await message.answer(f'Hello, {user.first_name}!')
