import sqlalchemy as sa

from . import base, columns


class Transaction(base.DbModelBase):
    __tablename__ = 'transactions'

    id = columns.UUID_ID.copy()
    user_id = sa.Column(sa.ForeignKey('users.id'), nullable=False)  # type: ignore

    created_at = columns.CREATED_AT.copy()
    updated_at = columns.UPDATED_AT.copy()

    at_date = sa.Column(sa.TIMESTAMP, nullable=False)
    category_id = sa.Column(sa.ForeignKey('categories.id'), nullable=False)  # type: ignore
    comment = sa.Column(sa.Text, nullable=True)

    outcome_account_id = sa.Column(sa.ForeignKey('accounts.id'), nullable=True)  # type: ignore
    outcome_currency = sa.Column(sa.Text, nullable=True)
    outcome = sa.Column(sa.Numeric, nullable=True)

    income_account_id = sa.Column(sa.ForeignKey('accounts.id'), nullable=True)  # type: ignore
    income_currency = sa.Column(sa.Text, nullable=True)
    income = sa.Column(sa.Numeric, nullable=True)
