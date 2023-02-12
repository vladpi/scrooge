from decimal import Decimal

from sqlalchemy.orm import Mapped

from . import base, columns


class Account(base.DbModelBase):
    __tablename__ = 'accounts'

    id: Mapped[columns.uuid_pk]
    workspace_id: Mapped[columns.workspaces_fk]

    created_at: Mapped[columns.created_at]
    updated_at: Mapped[columns.created_at]

    name: Mapped[str]

    balance: Mapped[Decimal]
    currency: Mapped[str]
