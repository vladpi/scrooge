import os
import pathlib

import sqlalchemy as sa
from litestar import Litestar

from app import db, tinkoff_csv
from app.consts import MOSCOW_TIMEZONE

TRANSACTIONS_CSV_PATH = pathlib.Path(os.environ["TRANSACTIONS_CSV_PATH"])

async def load_tinkoff_transactions(app: Litestar):
    async with db.config.get_session() as session:
        statement = sa.select(sa.func.count()).select_from(db.Transaction)
        count = await session.execute(statement)
        if not count.scalar():
            transactions = tinkoff_csv.parse_transactions_csv(TRANSACTIONS_CSV_PATH)

            for raw_transaction in transactions:
                session.add(
                    db.Transaction(
                        datetime=raw_transaction.transaction_datetime.replace(tzinfo=MOSCOW_TIMEZONE),
                        status=db.TransactionStatus(raw_transaction.status),
                        amount=raw_transaction.transaction_amount,
                        currency=raw_transaction.transaction_currency,
                        description=f"{raw_transaction.category} • {raw_transaction.description}",
                        tinkoff_transaction=raw_transaction.model_dump(),
                    )
                )

            await session.commit()


async def load_base_categories(app: Litestar):
    OUTCOME_CATEGORIES = [
        "🏠 Аренда квартиры",
        "📠 Коммунальные платежи",
        "🛒 Продукты и быт",
        "🚕 Такси и транспорт",
        "👖 Одежда, обувь, аксессуары",
        "🏥 Здоровье и спорт",
        "🧴 Уход за собой",
        "🍔 Доставка еды",
        "🧑‍🍳 Кафе и рестораны",
        "💻 Сервисы и подписки",
        "🎪 Развлечения",
        "🎁 Подарки",
        "📚 Образование",
        "🐕 Дарси",
        "🏝 Отпуск",
        "☕️ Кофе дома",
        "🚬 Сигареты",
        "📦 Прочее",
        "🏦 Кредиты",
    ]
    INCOME_CATEGORIES = [
        "💰 Зарплата",
        "🤑 Кэшбек и проценты",
        "🪙 Подработка",
    ]
    async with db.config.get_session() as session:
        statement = sa.select(sa.func.count()).select_from(db.Category)
        count = await session.execute(statement)
        if not count.scalar():
            for raw_category in OUTCOME_CATEGORIES:
                icon, name = raw_category.split(" ", maxsplit=1)
                session.add(db.Category(icon=icon, name=name, type=db.CategoryType.OUTCOME))
            for raw_category in INCOME_CATEGORIES:
                icon, name = raw_category.split(" ", maxsplit=1)
                session.add(db.Category(icon=icon, name=name, type=db.CategoryType.INCOME))
            session.add(db.Category(icon="", name="Без категории"))
            await session.commit()
