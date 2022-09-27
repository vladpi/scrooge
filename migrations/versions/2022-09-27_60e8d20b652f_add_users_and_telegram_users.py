"""Add users and telegram_users

Revision ID: 60e8d20b652f
Revises:
Create Date: 2022-09-27 15:29:51.650523

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '60e8d20b652f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute('CREATE EXTENSION IF NOT EXISTS pgcrypto;')

    op.create_table(
        'users',
        sa.Column(
            'id',
            postgresql.UUID(),
            server_default=sa.text('gen_random_uuid()'),
            nullable=False,
        ),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id', name=op.f('pk__users')),
    )
    op.create_table(
        'telegram_users',
        sa.Column('id', sa.BIGINT(), autoincrement=True, nullable=False),
        sa.Column('user_id', postgresql.UUID(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
        sa.Column('username', sa.Text(), nullable=True),
        sa.Column('first_name', sa.Text(), nullable=True),
        sa.Column('last_name', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(
            ['user_id'],
            ['users.id'],
            name=op.f('fk__telegram_users__user_id__users'),
        ),
        sa.PrimaryKeyConstraint('id', name=op.f('pk__telegram_users')),
        sa.UniqueConstraint('user_id', name=op.f('uq__telegram_users__user_id')),
    )


def downgrade() -> None:
    op.drop_table('telegram_users')
    op.drop_table('users')
