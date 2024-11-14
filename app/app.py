from datetime import datetime, timedelta
from pathlib import Path
from typing import TYPE_CHECKING

import sqlalchemy as sa
from dotenv import load_dotenv
from litestar import Litestar, get
from litestar.contrib.htmx.request import HTMXRequest
from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.di import Provide
from litestar.response import Template
from litestar.template.config import TemplateConfig

from app.utils import load_base_categories, load_tinkoff_transactions

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from app import db
from app.consts import MOSCOW_TIMEZONE, CategoryType
from app.models import Category, CategoryMonthBudget, MonthBudget
from app.routes import transactions_router

DEPENDENCIES = {
    "categories_repo": Provide(db.provide_categories_repo),
    "transactions_repo": Provide(db.provide_transactions_repo),
}


@get("/")
async def index(
    categories_repo: db.CategoriesRepository,
    transactions_repo: db.TransactionsRepository,
    db_session: "AsyncSession",
    db_engine: "AsyncEngine",
) -> Template:
    month_start = datetime.now(tz=MOSCOW_TIMEZONE).replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    month_start = month_start.replace(month=month_start.month - 1)
    month_end = month_start.replace(month=month_start.month + 1) - timedelta(days=1)

    categories_month_total = (
        sa.select(
            db.Transaction.category_id.label("category_id"),
            sa.func.sum(db.Transaction.amount).label("total_amount"),
        )
        .where(db.Transaction.category_id.isnot(None))
        .where(db.Transaction.status == db.TransactionStatus.OK)
        .where(db.Transaction.datetime.between(month_start, month_end))
        .group_by(db.Transaction.category_id)
    ).alias("categories_month_total")

    query = sa.select(
        db.Category,
        sa.func.coalesce(categories_month_total.c.total_amount, 0.0).label("total_amount"),
    ).select_from(
        sa.outerjoin(
            db.Category.__table__,
            categories_month_total,
            db.Category.id == categories_month_total.c.category_id,
        )
    )

    budget = MonthBudget(incomes=[], outcomes=[])
    async with db_engine.connect() as conn:
        for row in await conn.execute(query):
            category = Category(id=row.id, icon=row.icon, name=row.name, type=row.type, month_limit=row.month_limit)
            category_budget = CategoryMonthBudget(
                category=category,
                total_amount=row.total_amount,
            )
            if category.type == CategoryType.INCOME:
                budget.incomes.append(category_budget)
            elif category.type == CategoryType.OUTCOME:
                budget.outcomes.append(category_budget)

    return Template(template_name="index.html", context={"budget": budget})


# FIXME этому тут не место
load_dotenv()

app = Litestar(
    route_handlers=[index, transactions_router],
    request_class=HTMXRequest,
    template_config=TemplateConfig(
        directory=Path("templates"),
        engine=JinjaTemplateEngine,
    ),
    dependencies=DEPENDENCIES,
    debug=True,
    on_startup=[load_tinkoff_transactions, load_base_categories],
    plugins=[db.plugin],
)
