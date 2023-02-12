import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from . import base, columns


class Category(base.DbModelBase):
    __tablename__ = 'categories'

    id: Mapped[columns.uuid_pk]
    workspace_id: Mapped[columns.workspaces_fk]

    created_at: Mapped[columns.created_at]
    updated_at: Mapped[columns.updated_at]

    name: Mapped[str]

    is_income: Mapped[bool] = mapped_column(server_default=sa.true())
    is_outcome: Mapped[bool] = mapped_column(server_default=sa.true())
