from dataclasses import asdict

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncEngine

from domain.users import User, UserId

from . import models


def user_model_to_user(model: models.User) -> User:
    return User(
        id=UserId(str(model.id)),
        email=model.email,
        password_hash=model.password_hash,
        first_name=model.first_name,
        last_name=model.last_name,
        avatar_url=model.avatar_url,
    )


class SQLUsersRepository:
    def __init__(self, db_engine: AsyncEngine) -> None:
        self._db_engine = db_engine

    async def create_user(self, data: User) -> User:
        async with self._db_engine.begin() as conn:
            query = sa.insert(models.User).values(asdict(data)).returning(models.User)

            result = await conn.execute(query)
            row = result.one()

        return user_model_to_user(row)  # type: ignore

    async def get_user(self, user_id: UserId) -> User | None:
        async with self._db_engine.begin() as conn:
            query = sa.select(models.User).where(models.User.id == user_id)

            result = await conn.execute(query)
            row = result.one()

        if row is not None:
            return user_model_to_user(row)  # type: ignore

    async def get_user_by_email(self, email: str) -> User | None:
        async with self._db_engine.begin() as conn:
            query = sa.select(models.User).where(models.User.email == email)

            result = await conn.execute(query)
            row = result.one()

        if row is not None:
            return user_model_to_user(row)  # type: ignore
