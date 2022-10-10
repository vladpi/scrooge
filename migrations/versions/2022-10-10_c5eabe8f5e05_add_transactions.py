"""Add transactions

Revision ID: c5eabe8f5e05
Revises: cf3f91161c60
Create Date: 2022-10-10 23:41:32.053495

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'c5eabe8f5e05'
down_revision = 'cf3f91161c60'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'transactions',
        sa.Column(
            'id',
            postgresql.UUID(),
            server_default=sa.text('gen_random_uuid()'),
            nullable=False,
        ),
        sa.Column('user_id', postgresql.UUID(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
        sa.Column('at_date', sa.TIMESTAMP(), nullable=False),
        sa.Column('category_id', postgresql.UUID(), nullable=False),
        sa.Column('comment', sa.Text(), nullable=True),
        sa.Column('outcome_account_id', postgresql.UUID(), nullable=True),
        sa.Column('outcome_currency', sa.Text(), nullable=True),
        sa.Column('outcome', sa.Numeric(), nullable=True),
        sa.Column('income_account_id', postgresql.UUID(), nullable=True),
        sa.Column('income_currency', sa.Text(), nullable=True),
        sa.Column('income', sa.Numeric(), nullable=True),
        sa.ForeignKeyConstraint(
            ['category_id'],
            ['categories.id'],
            name=op.f('fk__transactions__category_id__categories'),
        ),
        sa.ForeignKeyConstraint(
            ['income_account_id'],
            ['accounts.id'],
            name=op.f('fk__transactions__income_account_id__accounts'),
        ),
        sa.ForeignKeyConstraint(
            ['outcome_account_id'],
            ['accounts.id'],
            name=op.f('fk__transactions__outcome_account_id__accounts'),
        ),
        sa.ForeignKeyConstraint(
            ['user_id'],
            ['users.id'],
            name=op.f('fk__transactions__user_id__users'),
        ),
        sa.PrimaryKeyConstraint('id', name=op.f('pk__transactions')),
    )


def downgrade() -> None:
    op.drop_table('transactions')
