import sqlalchemy as sa

from . import base, columns


class Category(base.DbModelBase):
    __tablename__ = 'categories'

    id = columns.UUID_ID.copy()
    workspace_id = sa.Column(sa.ForeignKey('workspaces.id'), nullable=False)  # type: ignore

    created_at = columns.CREATED_AT.copy()
    updated_at = columns.UPDATED_AT.copy()

    name = sa.Column(sa.Text, nullable=False)

    is_income = sa.Column(sa.Boolean, server_default=sa.true(), nullable=False)
    is_outcome = sa.Column(sa.Boolean, server_default=sa.true(), nullable=False)
