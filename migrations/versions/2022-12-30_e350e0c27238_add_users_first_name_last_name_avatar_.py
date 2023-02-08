"""Add users first_name last_name avatar_url

Revision ID: e350e0c27238
Revises: c5eabe8f5e05
Create Date: 2022-12-30 12:03:38.285606

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'e350e0c27238'
down_revision = 'c5eabe8f5e05'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('users', sa.Column('first_name', sa.Text(), nullable=True))
    op.add_column('users', sa.Column('last_name', sa.Text(), nullable=True))
    op.add_column('users', sa.Column('avatar_url', sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'avatar_url')
    op.drop_column('users', 'last_name')
    op.drop_column('users', 'first_name')
