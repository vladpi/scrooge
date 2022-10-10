from app import models, repositories

from .schemas import (
    CreateIncomeTransactionRequest,
    CreateOutcomeTransactionRequest,
    CreateTransferTransactionRequest,
)


async def create_income_transaction(
    repos: repositories.Repositories,
    request: CreateIncomeTransactionRequest,
) -> models.Transaction:
    return await _create_transaction(
        repos,
        models.IncomeTransactionCreate(
            user_id=request.user_id,
            at_date=request.at_date,
            category_id=request.category_id,
            comment=request.comment,
            income_account_id=request.account_id,
            income_currency=request.currency,
            income=request.amount,
        ),
    )


async def create_outcome_transaction(
    repos: repositories.Repositories,
    request: CreateOutcomeTransactionRequest,
) -> models.Transaction:
    return await _create_transaction(
        repos,
        models.OutcomeTransactionCreate(
            user_id=request.user_id,
            at_date=request.at_date,
            category_id=request.category_id,
            comment=request.comment,
            outcome_account_id=request.account_id,
            outcome_currency=request.currency,
            outcome=request.amount,
        ),
    )


async def create_transfer_transaction(
    repos: repositories.Repositories,
    request: CreateTransferTransactionRequest,
) -> models.Transaction:
    return await _create_transaction(
        repos,
        models.TransferTransactionCreate(
            user_id=request.user_id,
            at_date=request.at_date,
            category_id=request.category_id,
            comment=request.comment,
            outcome_account_id=request.outcome_account_id,
            outcome_currency=request.outcome_currency,
            outcome=request.outcome,
            income_account_id=request.income_account_id,
            income_currency=request.income_currency,
            income=request.income,
        ),
    )


async def _create_transaction(
    repos: repositories.Repositories,
    request: models.TransactionCreate,
) -> models.Transaction:
    transaction = await repos.transactions_repo.create(request)

    await _update_accounts_balance_from_transaction(
        repos.accounts_repo,
        transaction,
    )

    return transaction


async def _update_accounts_balance_from_transaction(
    accounts_repo: repositories.AccountsRepository,
    transaction: models.Transaction,
) -> None:
    if transaction.outcome_account_id is not None and transaction.outcome:
        await accounts_repo.update_balance(
            id_=transaction.outcome_account_id,
            diff=-1 * transaction.outcome,
        )

    if transaction.income_account_id is not None and transaction.income:
        await accounts_repo.update_balance(
            id_=transaction.income_account_id,
            diff=transaction.income,
        )
