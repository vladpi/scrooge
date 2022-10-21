from app import models, repositories

from .schemas import (
    CreateIncomeTransactionRequest,
    CreateOutcomeTransactionRequest,
    CreateTransferTransactionRequest,
)


class TransactionsService:  # noqa: WPS306
    def __init__(
        self,
        transactions_repo: repositories.TranasactionssRepository,
        accounts_repo: repositories.AccountsRepository,
    ) -> None:
        self._transactions_repo = transactions_repo
        self._accounts_repo = accounts_repo

    async def create_income_transaction(
        self,
        request: CreateIncomeTransactionRequest,
    ) -> models.Transaction:
        return await self.create_transaction(
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
        self,
        request: CreateOutcomeTransactionRequest,
    ) -> models.Transaction:
        return await self.create_transaction(
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
        self,
        request: CreateTransferTransactionRequest,
    ) -> models.Transaction:
        return await self.create_transaction(
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

    async def create_transaction(
        self,
        request: models.TransactionCreate,
    ) -> models.Transaction:
        transaction = await self._transactions_repo.create(request)
        await self._update_accounts_balance_from_transaction(transaction)
        return transaction

    async def _update_accounts_balance_from_transaction(
        self,
        transaction: models.Transaction,
    ) -> None:
        if transaction.outcome_account_id is not None and transaction.outcome:
            await self._accounts_repo.update_balance(
                id_=transaction.outcome_account_id,
                diff=-1 * transaction.outcome,
            )

        if transaction.income_account_id is not None and transaction.income:
            await self._accounts_repo.update_balance(
                id_=transaction.income_account_id,
                diff=transaction.income,
            )
