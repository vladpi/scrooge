"""Add accounts table

Revision ID: cf3f91161c60
Revises: 5ff97cdbec58
Create Date: 2022-10-01 01:23:03.411957

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'cf3f91161c60'
down_revision = '5ff97cdbec58'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'accounts',
        sa.Column(
            'id',
            postgresql.UUID(),
            server_default=sa.text('gen_random_uuid()'),
            nullable=False,
        ),
        sa.Column('workspace_id', postgresql.UUID(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
        sa.Column('name', sa.Text(), nullable=False),
        sa.Column('balance', sa.Numeric(), nullable=False),
        sa.Column('currency', sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(
            ['workspace_id'],
            ['workspaces.id'],
            name=op.f('fk__accounts__workspace_id__workspaces'),
        ),
        sa.PrimaryKeyConstraint('id', name=op.f('pk__accounts')),
    )


def downgrade() -> None:
    op.drop_table('accounts')
