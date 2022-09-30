from enum import Enum


class Currency(str, Enum):  # noqa: WPS600
    RUB = 'RUB'  # noqa: WPS115
    USD = 'USD'  # noqa: WPS115
    EUR = 'EUR'  # noqa: WPS115
