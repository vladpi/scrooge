from datetime import date
from decimal import Decimal
from typing import Optional

from .accounts import AccountId
from .base import BaseCreateRequest, BaseModel, BaseUpdateRequest, UUIDIdentity
from .categories import CategoryId
from .core import Currency
from .users import UserId


class TransactionId(UUIDIdentity):
    """Transaction ID"""


class Transaction(BaseModel):
    id: TransactionId
    user_id: UserId

    at_date: date
    category_id: CategoryId
    # category: Category  # FIXME
    comment: Optional[str] = None

    outcome_account_id: Optional[AccountId] = None
    # outcome_account: Optional[Account]  # FIXME
    outcome_currency: Optional[Currency] = None
    outcome: Optional[Decimal] = None

    income_account_id: Optional[AccountId] = None
    # income_account: Optional[Account]  # FIXME
    income_currency: Optional[Currency] = None
    income: Optional[Decimal] = None


class TransactionCreate(BaseCreateRequest):
    user_id: UserId

    at_date: date
    category_id: CategoryId
    comment: Optional[str] = None

    outcome_account_id: Optional[AccountId] = None
    outcome_currency: Optional[Currency] = None
    outcome: Optional[Decimal] = None

    income_account_id: Optional[AccountId] = None
    income_currency: Optional[Currency] = None
    income: Optional[Decimal] = None


class IncomeTransactionCreate(TransactionCreate):
    income_account_id: AccountId
    income_currency: Currency
    income: Decimal


class OutcomeTransactionCreate(TransactionCreate):
    outcome_account_id: AccountId
    outcome_currency: Currency
    outcome: Decimal


class TransferTransactionCreate(TransactionCreate):
    outcome_account_id: AccountId
    outcome_currency: Currency
    outcome: Decimal

    income_account_id: AccountId
    income_currency: Currency
    income: Decimal


class TransactionUpdate(BaseUpdateRequest):
    # TODO стоит пересмотреть это, когда вернусь к редактированию транзакций
    at_date: Optional[date] = None
    category_id: Optional[CategoryId] = None

    comment: Optional[str] = None

    outcome_account_id: Optional[AccountId] = None
    outcome_currency: Optional[Currency] = None
    outcome: Optional[Decimal] = None

    income_account_id: Optional[AccountId] = None
    income_currency: Optional[Currency] = None
    income: Optional[Decimal] = None
