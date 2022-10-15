from typing import List

from app import models, repositories

from .consts import DEFAULT_ACCOUNTS
from .schemas import CreateUserDefaultAccounts


async def create_user_defaults_accounts(
    accounts_repo: repositories.AccountsRepository,
    request: CreateUserDefaultAccounts,
) -> List[models.Account]:
    accounts = []

    for default_account_name in DEFAULT_ACCOUNTS:
        account = await accounts_repo.create(
            models.AccountCreate(
                workspace_id=request.workspace_id,
                name=default_account_name,
                currency=request.currency,
            ),
        )
        accounts.append(account)

    return accounts


async def get_workspace_accounts(
    repos: repositories.Repositories,
    workspace_id: models.WorkspaceId,
) -> List[models.Account]:
    return await repos.accounts_repo.get_by_workspace_id(workspace_id)


async def get_workspace_account_by_name(
    repos: repositories.Repositories,
    workspace_id: models.WorkspaceId,
    name: str,
) -> models.Account:
    return await repos.accounts_repo.get_by_workspace_id_and_name(workspace_id, name)
