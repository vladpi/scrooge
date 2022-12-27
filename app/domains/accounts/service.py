from app import models, repositories

from .consts import DEFAULT_ACCOUNTS
from .schemas import CreateUserDefaultAccounts, CreateWorkspaceAccount


class AccountsService:
    def __init__(self, accounts_repo: repositories.AccountsRepository) -> None:
        self._repo = accounts_repo

    async def create_user_defaults_accounts(
        self,
        request: CreateUserDefaultAccounts,
    ) -> list[models.Account]:
        accounts = []

        for default_account_name in DEFAULT_ACCOUNTS:
            account = await self._repo.create(
                models.AccountCreate(
                    workspace_id=request.workspace_id,
                    name=default_account_name,
                    currency=request.currency,
                ),
            )
            accounts.append(account)

        return accounts

    async def create_workspace_account(
        self,
        request: CreateWorkspaceAccount,
    ) -> models.Account:
        return await self._repo.create(
            models.AccountCreate(
                workspace_id=request.workspace_id,
                name=request.name,
                currency=request.currency,
            ),
        )

    async def get_workspace_accounts(
        self,
        workspace_id: models.WorkspaceId,
    ) -> list[models.Account]:
        return await self._repo.get_by_workspace_id(workspace_id)

    async def get_workspace_account_by_name(
        self,
        workspace_id: models.WorkspaceId,
        name: str,
    ) -> models.Account:
        return await self._repo.get_by_workspace_id_and_name(workspace_id, name)
