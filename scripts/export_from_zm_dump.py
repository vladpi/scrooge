import argparse
import asyncio
import logging
import pathlib

import databases
from pydantic import BaseModel

from app import models, repositories, settings
from app.adapters import zenmoney
from app.domains import (
    CreateWorkspaceAccount,
    CreateWorkspaceCategory,
    create_transaction,
    create_workspace_account,
    create_workspace_category,
    get_workspace_account_by_name,
    get_workspace_category_by_name,
)
from libs.context import ContextBase

logger = logging.getLogger(__name__)


class Args(BaseModel):
    dump_path: pathlib.Path
    user_id: str
    workspace_id: str


class Context(ContextBase):
    app_settings: settings.AppSettings

    db: databases.Database

    repos: repositories.Repositories

    async def _do_close(self) -> None:
        await self.db.disconnect()


async def make_context() -> Context:
    try:
        return await _make_context()

    except Exception:
        logger.exception('Failed to initialize bot context')
        raise


async def _make_context() -> Context:  # noqa: WPS210
    logger.info('Initializing bot context')

    app_settings = settings.AppSettings()
    db = databases.Database(app_settings.DATABASE_URL)
    await db.connect()

    users_repo = repositories.UsersRepositoryImpl(db)
    telegram_users_repo = repositories.TelegramUsersRepositoryImpl(db)
    workspaces_repo = repositories.WorkspacesRepositoryImpl(db)
    categories_repo = repositories.CategoriesRepositoryImpl(db)
    accounts_repo = repositories.AccountsRepositoryImpl(db)
    transactions_repo = repositories.TransactionsRepositoryImpl(db)

    return Context(
        app_settings=app_settings,
        db=db,
        repos=repositories.Repositories(
            users_repo=users_repo,
            telegram_users_repo=telegram_users_repo,
            workspaces_repo=workspaces_repo,
            categories_repo=categories_repo,
            accounts_repo=accounts_repo,
            transactions_repo=transactions_repo,
        ),
    )


async def main(args: Args) -> None:
    ctx = await make_context()
    user_id = models.UserId(args.user_id)
    workspace_id = models.WorkspaceId(args.workspace_id)

    zenmoney_transactions = zenmoney.parse_csv_dump(args.dump_path)
    for zm_transaction in zenmoney_transactions:
        await _create_transaction_from_zm(ctx, user_id, workspace_id, zm_transaction)


async def _create_transaction_from_zm(
    ctx: Context,
    user_id: models.UserId,
    workspace_id: models.WorkspaceId,
    zm_transaction: zenmoney.Transaction,
) -> models.Transaction:
    category = await _get_or_create_workspace_category(ctx, workspace_id, zm_transaction.category)

    outcome_account = await _get_or_create_workspace_account(
        ctx,
        workspace_id,
        zm_transaction.outcome_account,
    )
    income_account = await _get_or_create_workspace_account(
        ctx,
        workspace_id,
        zm_transaction.income_account,
    )

    return await create_transaction(
        ctx.repos,
        models.TransactionCreate(
            user_id=user_id,
            at_date=zm_transaction.at_date,
            category_id=category.id,
            comment=zm_transaction.comment,
            outcome_account_id=outcome_account.id if outcome_account else None,
            outcome_currency=outcome_account.currency if outcome_account else None,
            outcome=zm_transaction.outcome,
            income_account_id=income_account.id if income_account else None,
            income_currency=income_account.currency if income_account else None,
            income=zm_transaction.income,
            created_at=zm_transaction.created_at,
            updated_at=zm_transaction.updated_at,
        ),
    )


async def _get_or_create_workspace_category(
    ctx: Context,
    workspace_id: models.WorkspaceId,
    zm_category: zenmoney.Category,
) -> models.Category:
    try:
        return await get_workspace_category_by_name(ctx.repos, workspace_id, zm_category.name)
    except repositories.NotFoundError:
        return await create_workspace_category(
            ctx.repos,
            CreateWorkspaceCategory(
                workspace_id=workspace_id,
                name=zm_category.name,
            ),
        )


async def _get_or_create_workspace_account(
    ctx: Context,
    workspace_id: models.WorkspaceId,
    zm_account: zenmoney.Account | None,
) -> models.Account | None:
    if zm_account is None:
        return None

    try:
        return await get_workspace_account_by_name(ctx.repos, workspace_id, zm_account.name)
    except repositories.NotFoundError:
        return await create_workspace_account(
            ctx.repos,
            CreateWorkspaceAccount(
                workspace_id=workspace_id,
                name=zm_account.name,
                currency=zm_account.currency,
            ),
        )


def _parse_args() -> Args:
    parser = argparse.ArgumentParser()

    parser.add_argument('--dump-path', dest='dump_path', type=str)
    parser.add_argument('--user-id', dest='user_id', type=str)
    parser.add_argument('--workspace-id', dest='workspace_id', type=str)

    args = parser.parse_args()
    return Args(
        dump_path=args.dump_path,
        user_id=args.user_id,
        workspace_id=args.workspace_id,
    )


if __name__ == '__main__':
    asyncio.run(main(_parse_args()))
