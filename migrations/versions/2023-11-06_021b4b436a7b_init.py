"""Init

Revision ID: 021b4b436a7b
Revises:
Create Date: 2023-11-06 19:52:14.965381

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "021b4b436a7b"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto;")

    op.create_table(
        "users",
        sa.Column("id", sa.UUID(), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password_hash", sa.String(), nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.TIMESTAMP(), server_default=sa.text("now()"), nullable=False),
        sa.Column("first_name", sa.String(), nullable=True),
        sa.Column("last_name", sa.String(), nullable=True),
        sa.Column("avatar_url", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id", name=op.f("pk__users")),
    )
    op.create_table(
        "workspaces",
        sa.Column("id", sa.UUID(), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("owner_id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.TIMESTAMP(), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(
            ["owner_id"], ["users.id"], name=op.f("fk__workspaces__owner_id__users")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk__workspaces")),
    )
    op.create_table(
        "accounts",
        sa.Column("id", sa.UUID(), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("workspace_id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.TIMESTAMP(), server_default=sa.text("now()"), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("balance", sa.Numeric(), nullable=False),
        sa.Column("currency", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(
            ["workspace_id"], ["workspaces.id"], name=op.f("fk__accounts__workspace_id__workspaces")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk__accounts")),
    )
    op.create_table(
        "categories",
        sa.Column("id", sa.UUID(), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("workspace_id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.TIMESTAMP(), server_default=sa.text("now()"), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("is_income", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        sa.Column("is_outcome", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        sa.ForeignKeyConstraint(
            ["workspace_id"],
            ["workspaces.id"],
            name=op.f("fk__categories__workspace_id__workspaces"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk__categories")),
    )
    op.create_table(
        "transactions",
        sa.Column("id", sa.UUID(), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.TIMESTAMP(), server_default=sa.text("now()"), nullable=False),
        sa.Column("at_date", sa.DateTime(), nullable=False),
        sa.Column("category_id", sa.UUID(), nullable=False),
        sa.Column("comment", sa.String(), nullable=True),
        sa.Column("outcome_account_id", sa.UUID(), nullable=True),
        sa.Column("outcome_currency", sa.String(), nullable=True),
        sa.Column("outcome", sa.Numeric(), nullable=True),
        sa.Column("income_account_id", sa.UUID(), nullable=True),
        sa.Column("income_currency", sa.String(), nullable=True),
        sa.Column("income", sa.Numeric(), nullable=True),
        sa.ForeignKeyConstraint(
            ["category_id"],
            ["categories.id"],
            name=op.f("fk__transactions__category_id__categories"),
        ),
        sa.ForeignKeyConstraint(
            ["income_account_id"],
            ["accounts.id"],
            name=op.f("fk__transactions__income_account_id__accounts"),
        ),
        sa.ForeignKeyConstraint(
            ["outcome_account_id"],
            ["accounts.id"],
            name=op.f("fk__transactions__outcome_account_id__accounts"),
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], name=op.f("fk__transactions__user_id__users")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk__transactions")),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("transactions")
    op.drop_table("categories")
    op.drop_table("accounts")
    op.drop_table("workspaces")
    op.drop_table("users")
    # ### end Alembic commands ###
