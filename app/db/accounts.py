import sqlalchemy as sa

from . import base, columns


class Account(base.DbModelBase):
    __tablename__ = 'accounts'

    id = columns.UUID_ID.copy()
    workspace_id = sa.Column(sa.ForeignKey('workspaces.id'), nullable=False)  # type: ignore

    created_at = columns.CREATED_AT.copy()
    updated_at = columns.UPDATED_AT.copy()

    name = sa.Column(sa.Text, nullable=False)

    balance = sa.Column(sa.Numeric, nullable=False)
    currency = sa.Column(sa.Text, nullable=False)
