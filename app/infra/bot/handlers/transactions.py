from datetime import date, datetime, timedelta
from functools import partial
from typing import TYPE_CHECKING, Optional

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext, filters

from app import utils
from app.domains import CreateIncomeTransactionRequest, CreateOutcomeTransactionRequest
from app.repositories.exceptions import NotFoundError

from ..states import AddTransactionStates

if TYPE_CHECKING:
    from app.infra.bot.context import Context
    from app.models import TelegramUser, Workspace


TODAY = 'Сегодня'
YESTERDAY = 'Вчера'

TRANSACTION_PROXY_ATTR = 'transaction'


def setup_handlers(dispatcher: Dispatcher) -> None:
    dispatcher.register_message_handler(
        partial(txn_entry_handler, transaction_type='outcome'),
        filters.Command('outcome'),
        state='*',
    )
    dispatcher.register_message_handler(
        partial(txn_entry_handler, transaction_type='income'),
        filters.Command('income'),
        state='*',
    )
    dispatcher.register_message_handler(
        txn_account_handler,
        state=AddTransactionStates.account,
    )
    dispatcher.register_message_handler(
        txn_amount_and_comment_handler,
        state=AddTransactionStates.amount_and_comment,
    )
    dispatcher.register_message_handler(
        txn_at_date_handler,
        state=AddTransactionStates.at_date,
    )
    dispatcher.register_message_handler(
        txn_category_handler,
        state=AddTransactionStates.category,
    )


async def txn_entry_handler(  # noqa: WPS211
    message: types.Message,
    state: FSMContext,
    ctx: 'Context',
    user: 'TelegramUser',
    workspace: 'Workspace',
    transaction_type: str,
) -> None:
    async with state.proxy() as proxy:
        proxy['transaction'] = {
            'type': transaction_type,
            'user_id': str(user.user_id),
        }

    accounts = await ctx.services.accounts.get_workspace_accounts(workspace.id)
    keyboard = [[types.KeyboardButton(account.name)] for account in accounts]
    reply_markup = types.ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await message.answer(
        text='Выбери счет',
        reply_markup=reply_markup,
    )
    await AddTransactionStates.account.set()


async def txn_account_handler(
    message: types.Message,
    state: FSMContext,
    ctx: 'Context',
    user: 'TelegramUser',
    workspace: 'Workspace',
) -> None:
    try:
        account = await ctx.services.accounts.get_workspace_account_by_name(
            workspace.id,
            message.text,
        )

    except NotFoundError:
        return  # FIXME message

    async with state.proxy() as proxy:
        proxy[TRANSACTION_PROXY_ATTR]['account_id'] = str(account.id)
        proxy[TRANSACTION_PROXY_ATTR]['currency'] = account.currency.value

    await message.answer(
        text='Отправь сумму и комментарий',
        reply_markup=types.ReplyKeyboardRemove(),
    )
    await AddTransactionStates.amount_and_comment.set()


async def txn_amount_and_comment_handler(
    message: types.Message,
    state: FSMContext,
    ctx: 'Context',
    user: 'TelegramUser',
) -> None:
    amount, comment = utils.parse_amount_and_comment(message.text)

    if amount is None:
        await message.answer('Не вижу сумму.\nПовтори в формате: <pre>123.45</pre>')
        return

    async with state.proxy() as proxy:
        proxy[TRANSACTION_PROXY_ATTR]['amount'] = amount
        proxy[TRANSACTION_PROXY_ATTR]['comment'] = comment

    keyboard = [
        [types.KeyboardButton(YESTERDAY), types.KeyboardButton(TODAY)],
    ]
    reply_markup = types.ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await message.answer(
        text='Выбери или отправь дату',
        reply_markup=reply_markup,
    )
    await AddTransactionStates.at_date.set()


async def txn_at_date_handler(
    message: types.Message,
    state: FSMContext,
    ctx: 'Context',
    user: 'TelegramUser',
    workspace: 'Workspace',
) -> None:
    parsed_date: Optional[date]

    if message.text == TODAY:
        parsed_date = datetime.utcnow().date()  # FIXME localize date

    elif message.text == YESTERDAY:
        parsed_date = (datetime.utcnow() - timedelta(days=1)).date()  # FIXME localize date

    else:
        parsed_date = utils.parse_date(message.text)

    if parsed_date is None:
        await message.answer('Не вижу даты.\nПовтори в формате: <pre>01.02.20</pre>')
        return

    async with state.proxy() as proxy:
        proxy[TRANSACTION_PROXY_ATTR]['at_date'] = parsed_date.strftime('%Y-%m-%d')

    categories = await ctx.services.categories.get_workspace_categories(workspace.id)
    keyboard = [[types.KeyboardButton(category.name)] for category in categories]
    reply_markup = types.ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await message.answer(
        text='Выбери категорию',
        reply_markup=reply_markup,
    )
    await AddTransactionStates.category.set()


async def txn_category_handler(
    message: types.Message,
    state: FSMContext,
    ctx: 'Context',
    user: 'TelegramUser',
    workspace: 'Workspace',
) -> None:
    try:
        category = await ctx.services.categories.get_workspace_category_by_name(
            workspace.id,
            message.text,
        )
    except NotFoundError:
        return  # FIXME message

    async with state.proxy() as proxy:
        proxy[TRANSACTION_PROXY_ATTR]['category_id'] = str(category.id)

        transaction_data = proxy.pop(TRANSACTION_PROXY_ATTR)
        transaction_type = transaction_data.pop('type')

        if transaction_type == 'income':
            await ctx.services.transactions.create_income_transaction(
                CreateIncomeTransactionRequest(**transaction_data),
            )

        elif transaction_type == 'outcome':
            await ctx.services.transactions.create_outcome_transaction(
                CreateOutcomeTransactionRequest(**transaction_data),
            )

        else:
            return  # FIXME message

    await message.answer(
        text='Операция добавлена!',
        reply_markup=types.ReplyKeyboardRemove(),
    )
    await state.finish()
