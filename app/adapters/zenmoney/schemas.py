from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel


class Category(BaseModel):
    name: str


class Account(BaseModel):
    name: str
    currency: str  # FIXME or Currency type?


class Transaction(BaseModel):
    at_date: date

    category: Category
    comment: str | None = None

    income: Decimal | None = None
    income_account: Account | None = None
    outcome: Decimal | None = None
    outcome_account: Account | None = None

    created_at: datetime
    updated_at: datetime
