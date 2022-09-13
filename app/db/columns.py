import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# to reuse these columns, use .copy() method

UUID_ID = sa.Column(
    'id',
    postgresql.UUID,
    primary_key=True,
    server_default=sa.text('gen_random_uuid()'),
)

INT_ID = sa.Column(
    'id',
    sa.BIGINT,
    primary_key=True,
    autoincrement=True,
)

CREATED_AT = sa.Column(
    'created_at',
    sa.TIMESTAMP,
    server_default=sa.func.now(),
    nullable=False,
)

UPDATED_AT = sa.Column(
    'updated_at',
    sa.TIMESTAMP,
    server_default=sa.func.now(),
    onupdate=sa.func.now(),
    nullable=False,
)
