from typing import TYPE_CHECKING

from litestar import Router, get, post
from litestar.contrib.htmx.request import HTMXRequest
from litestar.contrib.htmx.response import HTMXTemplate
from litestar.response import Template

if TYPE_CHECKING:
    pass

from app import db


@get("/")
async def get_transactions(transactions_repo: db.TransactionsRepository) -> Template:
    unsorted_transactions_count = await transactions_repo.count(db.Transaction.category_id.is_(None))
    context = {"unsorted_transactions_count": unsorted_transactions_count}
    return HTMXTemplate(
        template_name="transactions/index.html",
        context=context,
    )


@get("/sorted")
async def get_sorted_transactions(
    transactions_repo: db.TransactionsRepository,
) -> Template:
    transactions = await transactions_repo.list(
        db.Transaction.category_id.is_not(None),
        order_by=(db.Transaction.datetime, False),
    )

    context = {"transactions": transactions}
    return HTMXTemplate(
        template_name="transactions/partial/sorted_transactions.html",
        context=context,
    )


@get("/unsorted")
async def get_unsorted_transactions(
    categories_repo: db.CategoriesRepository,
    transactions_repo: db.TransactionsRepository,
) -> Template:
    categories = await categories_repo.list()
    transactions = await transactions_repo.list(
        db.Transaction.category_id.is_(None), order_by=(db.Transaction.datetime, False)
    )

    context = {"transactions": transactions, "categories": categories}
    return HTMXTemplate(
        template_name="transactions/partial/unsorted_transactions.html",
        context=context,
    )


@post("/{transaction_id:int}/category/{category_id:int}")
async def update_transaction_category(
    transaction_id: int,
    category_id: int,
    request: HTMXRequest,
    categories_repo: db.CategoriesRepository,
    transactions_repo: db.TransactionsRepository,
) -> Template:
    transaction = await transactions_repo.get(transaction_id)
    transaction.category_id = category_id
    await transactions_repo.update(transaction, auto_commit=True)

    categories = await categories_repo.list()
    transactions = await transactions_repo.list(
        db.Transaction.category_id.is_(None), order_by=(db.Transaction.datetime, False)
    )

    context = {"transactions": transactions, "categories": categories}
    return HTMXTemplate(
        template_name="transactions/partial/unsorted_transactions.html",
        context=context,
    )


transactions_router = Router(
    path="/transactions",
    route_handlers=[
        get_transactions,
        get_sorted_transactions,
        get_unsorted_transactions,
        update_transaction_category,
    ],
)
