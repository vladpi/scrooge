import sqlalchemy as sa

from . import base, columns


class Workspace(base.DbModelBase):
    __tablename__ = 'workspaces'

    id = columns.UUID_ID.copy()
    owner_id = sa.Column(
        sa.ForeignKey('users.id'),
        nullable=False,
    )  # type: ignore

    created_at = columns.CREATED_AT.copy()
    updated_at = columns.UPDATED_AT.copy()
