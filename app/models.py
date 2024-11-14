from dataclasses import dataclass
from decimal import Decimal

from app.consts import CategoryType


@dataclass
class Category:
    id: int
    icon: str
    name: str
    type: CategoryType | None
    month_limit: Decimal | None


@dataclass
class CategoryMonthBudget:
    category: Category
    total_amount: Decimal


@dataclass
class MonthBudget:
    incomes: list[CategoryMonthBudget]
    outcomes: list[CategoryMonthBudget]
