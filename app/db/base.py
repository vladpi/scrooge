import typing

import sqlalchemy as sa
from sqlalchemy.orm import DeclarativeBase


class DbModelProto(typing.Protocol):
    __table__: sa.Table


# Default naming convention for all indexes and constraints
# See why this is important and how it would save your time:
# https://alembic.sqlalchemy.org/en/latest/naming.html
convention = {
    'all_column_names': lambda constraint, table: '_'.join(
        [column.name for column in constraint.columns.values()],
    ),
    'ix': 'ix__%(table_name)s__%(all_column_names)s',
    'uq': 'uq__%(table_name)s__%(all_column_names)s',
    'ck': 'ck__%(table_name)s__%(constraint_name)s',
    'fk': 'fk__%(table_name)s__%(all_column_names)s__%(referred_table_name)s',
    'pk': 'pk__%(table_name)s',
}


METADATA = sa.MetaData(naming_convention=convention)  # type: ignore


class DbModelBase(DeclarativeBase):
    metadata = METADATA
