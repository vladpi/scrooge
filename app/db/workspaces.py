from sqlalchemy.orm import Mapped

from . import base, columns


class Workspace(base.DbModelBase):
    __tablename__ = 'workspaces'

    id: Mapped[columns.uuid_pk]
    owner_id: Mapped[columns.users_fk]

    created_at: Mapped[columns.created_at]
    updated_at: Mapped[columns.updated_at]
