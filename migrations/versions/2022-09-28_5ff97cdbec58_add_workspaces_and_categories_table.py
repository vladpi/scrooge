"""Add workspaces and categories table

Revision ID: 5ff97cdbec58
Revises: 60e8d20b652f
Create Date: 2022-09-28 23:35:38.850671

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '5ff97cdbec58'
down_revision = '60e8d20b652f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'workspaces',
        sa.Column(
            'id',
            postgresql.UUID(),
            server_default=sa.text('gen_random_uuid()'),
            nullable=False,
        ),
        sa.Column('owner_id', postgresql.UUID(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(
            ['owner_id'],
            ['users.id'],
            name=op.f('fk__workspaces__owner_id__users'),
        ),
        sa.PrimaryKeyConstraint('id', name=op.f('pk__workspaces')),
    )
    op.create_table(
        'categories',
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
        sa.Column('is_income', sa.Boolean(), server_default=sa.text('true'), nullable=False),
        sa.Column('is_outcome', sa.Boolean(), server_default=sa.text('true'), nullable=False),
        sa.ForeignKeyConstraint(
            ['workspace_id'],
            ['workspaces.id'],
            name=op.f('fk__categories__workspace_id__workspaces'),
        ),
        sa.PrimaryKeyConstraint('id', name=op.f('pk__categories')),
    )


def downgrade() -> None:
    op.drop_table('categories')
    op.drop_table('workspaces')
