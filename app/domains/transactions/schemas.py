from datetime import date
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel

from app import models


class _CreatTransactionRequest(BaseModel):
    user_id: models.UserId

    at_date: date
    category_id: models.CategoryId
    comment: Optional[str] = None

    account_id: models.AccountId
    currency: models.Currency
    amount: Decimal


class CreateIncomeTransactionRequest(_CreatTransactionRequest):
    """Create Income Transaction Request"""


class CreateOutcomeTransactionRequest(_CreatTransactionRequest):
    """Create Outcome Transaction Request"""


class CreateTransferTransactionRequest(BaseModel):
    user_id: models.UserId

    at_date: date
    category_id: models.CategoryId
    comment: Optional[str] = None

    outcome_account_id: models.AccountId
    outcome_currency: models.Currency
    outcome: Decimal

    income_account_id: models.AccountId
    income_currency: models.Currency
    income: Decimal
