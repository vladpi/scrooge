import sqlalchemy as sa

from . import base, columns


class User(base.DbModelBase):
    __tablename__ = 'users'

    id = columns.UUID_ID.copy()
    created_at = columns.CREATED_AT.copy()
    updated_at = columns.UPDATED_AT.copy()


class TelegramUser(base.DbModelBase):
    __tablename__ = 'telegram_users'

    id = columns.INT_ID.copy()
    user_id = sa.Column(
        sa.ForeignKey('users.id'),
        nullable=False,
        unique=True,
    )  # type: ignore

    created_at = columns.CREATED_AT.copy()
    updated_at = columns.UPDATED_AT.copy()

    username = sa.Column(sa.Text)
    first_name = sa.Column(sa.Text)
    last_name = sa.Column(sa.Text)
