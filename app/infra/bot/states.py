from aiogram.dispatcher.filters.state import State, StatesGroup


class AddTransactionStates(StatesGroup):
    account = State()
    amount_and_comment = State()
    at_date = State()
    category = State()
