import enum
from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from litestar.contrib.sqlalchemy.base import BigIntBase
from litestar.contrib.sqlalchemy.repository import SQLAlchemyAsyncRepository
from litestar.plugins.sqlalchemy import SQLAlchemyAsyncConfig, SQLAlchemyPlugin
from sqlalchemy import JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.consts import CategoryType

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

config = SQLAlchemyAsyncConfig(
    connection_string="sqlite+aiosqlite:///db.sqlite",
    create_all=True,
)
plugin = SQLAlchemyPlugin(config=config)


class Category(BigIntBase):
    __tablename__ = "categories"

    icon: Mapped[str]
    name: Mapped[str]
    type: Mapped[CategoryType | None]
    month_limit: Mapped[Decimal | None]


class TransactionStatus(str, enum.Enum):
    OK = "OK"
    FAILED = "FAILED"


class Transaction(BigIntBase):
    __tablename__ = "transactions"

    datetime: Mapped[datetime]
    status: Mapped[TransactionStatus]
    amount: Mapped[Decimal]
    currency: Mapped[str]
    category_id: Mapped[int | None] = mapped_column(ForeignKey("categories.id"))
    description: Mapped[str]

    tinkoff_transaction: Mapped[JSON] = mapped_column(type_=JSON)


class CategoriesRepository(SQLAlchemyAsyncRepository[Category]):
    model_type = Category


class TransactionsRepository(SQLAlchemyAsyncRepository[Transaction]):
    model_type = Transaction


async def provide_categories_repo(db_session: "AsyncSession") -> CategoriesRepository:
    return CategoriesRepository(session=db_session)


async def provide_transactions_repo(db_session: "AsyncSession") -> TransactionsRepository:
    return TransactionsRepository(session=db_session)
