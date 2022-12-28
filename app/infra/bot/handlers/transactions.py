from datetime import date, datetime, timedelta
from functools import partial
from typing import TYPE_CHECKING, Optional

from aiogram import Dispatcher, filters, types
from aiogram.fsm.context import FSMContext
from neoteroi import di

from app import domains, utils
from app.repositories.exceptions import NotFoundError

from ..states import AddTransactionStates

if TYPE_CHECKING:
    from app.models import TelegramUser, Workspace


TODAY = 'Сегодня'
YESTERDAY = 'Вчера'

TRANSACTION_PROXY_ATTR = 'transaction'


def setup_handlers(dispatcher: Dispatcher) -> None:
    dispatcher.message.register(
        partial(txn_entry_handler, transaction_type='outcome'),
        filters.Command('outcome'),
    )
    dispatcher.message.register(
        partial(txn_entry_handler, transaction_type='income'),
        filters.Command('income'),
    )
    dispatcher.message.register(
        txn_account_handler,
        AddTransactionStates.account,
    )
    dispatcher.message.register(
        txn_amount_and_comment_handler,
        AddTransactionStates.amount_and_comment,
    )
    dispatcher.message.register(
        txn_at_date_handler,
        AddTransactionStates.at_date,
    )
    dispatcher.message.register(
        txn_category_handler,
        AddTransactionStates.category,
    )


async def txn_entry_handler(  # noqa: WPS211
    message: types.Message,
    state: FSMContext,
    container: di.Container,
    user: 'TelegramUser',
    workspace: 'Workspace',
    transaction_type: str,
) -> None:
    await state.update_data(
        user_id=str(user.user_id),
        type=transaction_type,
    )

    accounts_service = container.resolve(domains.AccountsService)
    accounts = await accounts_service.get_workspace_accounts(workspace.id)

    keyboard = [[types.KeyboardButton(text=account.name)] for account in accounts]
    reply_markup = types.ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
    await message.answer(
        text='Выбери счет',
        reply_markup=reply_markup,
    )
    await state.set_state(AddTransactionStates.account)


async def txn_account_handler(
    message: types.Message,
    state: FSMContext,
    container: di.Container,
    user: 'TelegramUser',
    workspace: 'Workspace',
) -> None:
    accounts_service = container.resolve(domains.AccountsService)

    try:
        account = await accounts_service.get_workspace_account_by_name(
            workspace.id,
            message.text,
        )

    except NotFoundError:
        return  # FIXME message

    await state.update_data(
        account_id=str(account.id),
        currency=account.currency.value,
    )

    await message.answer(
        text='Отправь сумму и комментарий',
        reply_markup=types.ReplyKeyboardRemove(),
    )
    await state.set_state(AddTransactionStates.amount_and_comment)


async def txn_amount_and_comment_handler(
    message: types.Message,
    state: FSMContext,
    container: di.Container,
    user: 'TelegramUser',
) -> None:
    amount, comment = utils.parse_amount_and_comment(message.text)

    if amount is None:
        await message.answer('Не вижу сумму.\nПовтори в формате: <pre>123.45</pre>')
        return

    await state.update_data(amount=amount, comment=comment)

    keyboard = [
        [types.KeyboardButton(text=YESTERDAY), types.KeyboardButton(text=TODAY)],
    ]
    reply_markup = types.ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

    await message.answer(
        text='Выбери или отправь дату',
        reply_markup=reply_markup,
    )
    await state.set_state(AddTransactionStates.at_date)


async def txn_at_date_handler(
    message: types.Message,
    state: FSMContext,
    container: di.Container,
    user: 'TelegramUser',
    workspace: 'Workspace',
) -> None:
    parsed_date = _parse_date(message.text)

    if parsed_date is None:
        await message.answer('Не вижу даты.\nПовтори в формате: <pre>01.02.20</pre>')
        return

    await state.update_data(at_date=parsed_date.strftime('%Y-%m-%d'))

    categories_service = container.resolve(domains.CategoriesService)
    categories = await categories_service.get_workspace_categories(workspace.id)
    keyboard = [[types.KeyboardButton(text=category.name)] for category in categories]
    reply_markup = types.ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
    await message.answer(
        text='Выбери категорию',
        reply_markup=reply_markup,
    )
    await state.set_state(AddTransactionStates.category)


def _parse_date(raw_date: Optional[str]) -> Optional[date]:
    parsed_date: Optional[date]

    if raw_date == TODAY:
        parsed_date = datetime.utcnow().date()  # FIXME localize date

    elif raw_date == YESTERDAY:
        parsed_date = (datetime.utcnow() - timedelta(days=1)).date()  # FIXME localize date

    else:
        parsed_date = utils.parse_date(raw_date)

    return parsed_date


async def txn_category_handler(
    message: types.Message,
    state: FSMContext,
    container: di.Container,
    user: 'TelegramUser',
    workspace: 'Workspace',
) -> None:
    categories_service = container.resolve(domains.CategoriesService)

    try:
        category = await categories_service.get_workspace_category_by_name(
            workspace.id,
            message.text,
        )
    except NotFoundError:
        return  # FIXME message

    await state.update_data(category_id=str(category.id))

    await _create_transaction_from_state(container, state)

    await message.answer(
        text='Операция добавлена!',
        reply_markup=types.ReplyKeyboardRemove(),
    )
    await state.clear()


async def _create_transaction_from_state(container: di.Container, state: FSMContext) -> None:
    transactions_service = container.resolve(domains.TransactionsService)

    transaction_data = await state.get_data()
    transaction_type = transaction_data.pop('type')

    # FIXME переместить эту логику в сервисный слой
    if transaction_type == 'income':
        await transactions_service.create_income_transaction(
            domains.CreateIncomeTransactionRequest(**transaction_data),
        )

    elif transaction_type == 'outcome':
        await transactions_service.create_outcome_transaction(
            domains.CreateOutcomeTransactionRequest(**transaction_data),
        )

    else:
        return  # FIXME message
