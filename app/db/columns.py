from datetime import datetime
from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import mapped_column
from typing_extensions import Annotated

uuid_pk = Annotated[
    UUID,
    mapped_column(
        postgresql.UUID,
        primary_key=True,
        server_default=sa.text('gen_random_uuid()'),
    ),
]


int_pk = Annotated[
    int,
    mapped_column(
        sa.BIGINT,
        primary_key=True,
        autoincrement=True,
    ),
]


created_at = Annotated[
    datetime,
    mapped_column(
        sa.TIMESTAMP,
        server_default=sa.func.now(),
        nullable=False,
    ),
]

updated_at = Annotated[
    datetime,
    mapped_column(
        sa.TIMESTAMP,
        server_default=sa.func.now(),
        onupdate=sa.func.now(),
        nullable=False,
    ),
]


users_fk = Annotated[
    UUID,
    mapped_column(
        sa.ForeignKey('users.id'),
        nullable=False,
    ),
]


workspaces_fk = Annotated[
    UUID,
    mapped_column(
        sa.ForeignKey('workspaces.id'),
        nullable=False,
    ),
]

categories_fk = Annotated[
    UUID,
    mapped_column(
        sa.ForeignKey('categories.id'),
        nullable=False,
    ),
]

accounts_fk = Annotated[
    UUID,
    mapped_column(
        sa.ForeignKey('accounts.id'),
        nullable=False,
    ),
]
