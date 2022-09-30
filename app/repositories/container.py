from pydantic import BaseModel

from .accounts import AccountsRepository
from .categories import CategoriesRepository
from .users import TelegramUsersRepository, UsersRepository
from .workspaces import WorkspacesRepository


class Repositories(BaseModel):
    users_repo: UsersRepository
    telegram_users_repo: TelegramUsersRepository
    workspaces_repo: WorkspacesRepository
    categories_repo: CategoriesRepository
    accounts_repo: AccountsRepository

    class Config:  # noqa: WPS306, WPS431
        arbitrary_types_allowed = True
        allow_mutation = False
