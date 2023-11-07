from datetime import datetime
from decimal import Decimal

import sqlalchemy as sa
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from . import columns

# Default naming convention for all indexes and constraints
# See why this is important and how it would save your time:
# https://alembic.sqlalchemy.org/en/latest/naming.html
convention = {
    "all_column_names": lambda constraint, table: "_".join(
        [column.name for column in constraint.columns.values()],
    ),
    "ix": "ix__%(table_name)s__%(all_column_names)s",
    "uq": "uq__%(table_name)s__%(all_column_names)s",
    "ck": "ck__%(table_name)s__%(constraint_name)s",
    "fk": "fk__%(table_name)s__%(all_column_names)s__%(referred_table_name)s",
    "pk": "pk__%(table_name)s",
}


METADATA = sa.MetaData(naming_convention=convention)  # type: ignore


class DbModelBase(DeclarativeBase):
    metadata = METADATA


class User(DbModelBase):
    __tablename__ = "users"

    id: Mapped[columns.uuid_pk]

    email: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str]

    created_at: Mapped[columns.created_at]
    updated_at: Mapped[columns.updated_at]

    first_name: Mapped[str | None]
    last_name: Mapped[str | None]

    avatar_url: Mapped[str | None]


class Workspace(DbModelBase):
    __tablename__ = "workspaces"

    id: Mapped[columns.uuid_pk]
    owner_id: Mapped[columns.users_fk]

    created_at: Mapped[columns.created_at]
    updated_at: Mapped[columns.updated_at]


class Category(DbModelBase):
    __tablename__ = "categories"

    id: Mapped[columns.uuid_pk]
    workspace_id: Mapped[columns.workspaces_fk]

    created_at: Mapped[columns.created_at]
    updated_at: Mapped[columns.updated_at]

    name: Mapped[str]

    is_income: Mapped[bool] = mapped_column(server_default=sa.true())
    is_outcome: Mapped[bool] = mapped_column(server_default=sa.true())


class Account(DbModelBase):
    __tablename__ = "accounts"

    id: Mapped[columns.uuid_pk]
    workspace_id: Mapped[columns.workspaces_fk]

    created_at: Mapped[columns.created_at]
    updated_at: Mapped[columns.created_at]

    name: Mapped[str]

    balance: Mapped[Decimal]
    currency: Mapped[str]


class Transaction(DbModelBase):
    __tablename__ = "transactions"

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
