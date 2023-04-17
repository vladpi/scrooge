from sqlalchemy.orm import Mapped, mapped_column

from . import base, columns


class User(base.DbModelBase):
    __tablename__ = 'users'

    id: Mapped[columns.uuid_pk]

    created_at: Mapped[columns.created_at]
    updated_at: Mapped[columns.updated_at]

    first_name: Mapped[str | None]
    last_name: Mapped[str | None]

    avatar_url: Mapped[str | None]


class TelegramUser(base.DbModelBase):
    __tablename__ = 'telegram_users'

    id: Mapped[columns.int_pk]
    user_id: Mapped[columns.users_fk] = mapped_column(unique=True)

    created_at: Mapped[columns.created_at]
    updated_at: Mapped[columns.updated_at]

    username: Mapped[str | None]
    first_name: Mapped[str | None]
    last_name: Mapped[str | None]
