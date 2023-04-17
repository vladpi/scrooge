from datetime import datetime
from decimal import Decimal

from sqlalchemy.orm import Mapped, mapped_column

from . import base, columns


class Transaction(base.DbModelBase):
    __tablename__ = 'transactions'

    id: Mapped[columns.uuid_pk]
    user_id: Mapped[columns.users_fk]

    created_at: Mapped[columns.created_at]
    updated_at: Mapped[columns.created_at]

    at_date: Mapped[datetime]
    category_id: Mapped[columns.categories_fk]
    comment: Mapped[str | None]

    outcome_account_id: Mapped[columns.accounts_fk] = mapped_column(nullable=True)
    outcome_currency: Mapped[str | None]
    outcome: Mapped[Decimal | None]

    income_account_id: Mapped[columns.accounts_fk] = mapped_column(nullable=True)
    income_currency: Mapped[str | None]
    income: Mapped[Decimal | None]
