from dataclasses import dataclass
from typing import Protocol
from uuid import UUID, uuid4

from .passwords import PasswordsService


class UserId(UUID):
    """User ID"""


@dataclass
class User:
    id: UserId

    email: str
    password_hash: str

    first_name: str | None = None
    last_name: str | None = None

    avatar_url: str | None = None

    @property
    def full_name(self) -> str:
        return " ".join(filter(None, [self.first_name, self.last_name]))


@dataclass
class CreateUserInput:
    email: str
    password: str

    first_name: str | None = None
    last_name: str | None = None

    avatar_url: str | None = None


@dataclass
class UpdateUserInput:
    first_name: str | None = None
    last_name: str | None = None

    avatar_url: str | None = None


class UsersRepository(Protocol):
    async def get_user(self, user_id: UserId) -> User | None:
        pass

    async def create_user(self, data: User) -> User:
        pass


class UsersService:
    def __init__(
        self, users_repository: UsersRepository, passwords_service: PasswordsService
    ) -> None:
        self.users_repository = users_repository
        self.passwords_service = passwords_service

    async def create_user(self, data: CreateUserInput) -> User:
        # FIXME check user with same email

        user = await self.users_repository.create_user(
            User(
                id=UserId(str(uuid4())),
                email=data.email,
                password_hash=self.passwords_service.hash_password(data.password),
                first_name=data.first_name,
                last_name=data.last_name,
                avatar_url=data.avatar_url,
            )
        )

        return user

    async def get_user(self, user_id: UserId) -> User:
        user = await self.users_repository.get_user(user_id)

        if user is None:
            raise ValueError("User not found")  # FIXME custom exception

        return user
