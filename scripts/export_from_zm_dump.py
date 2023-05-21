import argparse
import asyncio
import logging
import pathlib

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from app import models, repositories, settings
from app.adapters import zenmoney
from app.domains import (
    AccountsService,
    CategoriesService,
    CreateWorkspaceAccount,
    CreateWorkspaceCategory,
    TransactionsService,
)
from libs.context import ContextBase

logger = logging.getLogger(__name__)


class Args(BaseModel):
    dump_path: pathlib.Path
    user_id: str
    workspace_id: str


class Context(ContextBase):
    app_settings: settings.AppSettings

    db_engine: AsyncEngine

    categories_srv: CategoriesService
    accounts_srv: AccountsService
    transactions_srv: TransactionsService

    async def _do_close(self) -> None:
        await self.db_engine.dispose()


async def make_context() -> Context:
    try:
        return await _make_context()

    except Exception:
        logger.exception('Failed to initialize bot context')
        raise


async def _make_context() -> Context:  # noqa: WPS210
    logger.info('Initializing bot context')

    app_settings = settings.AppSettings()

    db_engine = create_async_engine(
        url=app_settings.DATABASE_URL,
        echo=True,
    )

    categories_repo = repositories.CategoriesRepositoryImpl(db_engine)
    accounts_repo = repositories.AccountsRepositoryImpl(db_engine)
    transactions_repo = repositories.TransactionsRepositoryImpl(db_engine)

    categories_srv = CategoriesService(categories_repo)
    accounts_srv = AccountsService(accounts_repo)
    transactions_srv = TransactionsService(transactions_repo, accounts_repo)

    return Context(
        app_settings=app_settings,
        db_engine=db_engine,
        categories_srv=categories_srv,
        accounts_srv=accounts_srv,
        transactions_srv=transactions_srv,
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

    return await ctx.transactions_srv.create_transaction(
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
        return await ctx.categories_srv.get_workspace_category_by_name(
            workspace_id,
            zm_category.name,
        )
    except repositories.NotFoundError:
        return await ctx.categories_srv.create_workspace_category(
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
        return await ctx.accounts_srv.get_workspace_account_by_name(workspace_id, zm_account.name)
    except repositories.NotFoundError:
        return await ctx.accounts_srv.create_workspace_account(
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
