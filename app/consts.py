import enum
from datetime import timedelta, timezone

MOSCOW_TIMEZONE = timezone(timedelta(hours=3), "Europe/Moscow")


class CategoryType(enum.Enum):
    INCOME = "INCOME"
    OUTCOME = "OUTCOME"
