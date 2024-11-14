import csv
import decimal
import pathlib
from datetime import date, datetime
from typing import Sequence

import pydantic


class tinkoff_datetime(datetime):
    @classmethod
    def __get_validators__(cls):
        yield cls.parse

    @classmethod
    def parse(cls, v, *args):
        if not v:
            return None
        return datetime.strptime(v, "%d.%m.%Y %H:%M:%S")


class tinkoff_date(date):
    @classmethod
    def __get_validators__(cls):
        yield cls.parse

    @classmethod
    def parse(cls, v, *args):
        if not v:
            return None
        return datetime.strptime(v, "%d.%m.%Y").date()


class tinkoff_decimal(decimal.Decimal):
    @classmethod
    def __get_validators__(cls):
        yield cls.parse

    @classmethod
    def parse(cls, v, *args):
        if not v:
            return None
        return decimal.Decimal(v.replace(",", "."))


class TinkoffTransaction(pydantic.BaseModel):
    transaction_datetime: tinkoff_datetime = pydantic.Field(alias="Дата операции")
    payment_date: tinkoff_date | None = pydantic.Field(alias="Дата платежа")
    card_number: str = pydantic.Field(alias="Номер карты")
    status: str = pydantic.Field(alias="Статус")
    transaction_amount: tinkoff_decimal = pydantic.Field(alias="Сумма операции")
    transaction_currency: str = pydantic.Field(alias="Валюта операции")
    payment_amount: tinkoff_decimal = pydantic.Field(alias="Сумма платежа")
    payment_currency: str = pydantic.Field(alias="Валюта платежа")
    cashback: tinkoff_decimal = pydantic.Field(alias="Кэшбэк")
    category: str = pydantic.Field(alias="Категория")
    mcc: str = pydantic.Field(alias="MCC")
    description: str = pydantic.Field(alias="Описание")
    bonuses_include_cashback: tinkoff_decimal = pydantic.Field(alias="Бонусы (включая кэшбэк)")
    rounding_to_investment_bank: tinkoff_decimal = pydantic.Field(alias="Округление на инвесткопилку")
    transaction_amount_with_rounding: tinkoff_decimal = pydantic.Field(alias="Сумма операции с округлением")


def parse_transactions_csv(csv_path: pathlib.Path) -> Sequence[TinkoffTransaction]:
    with csv_path.open("r", encoding="windows-1251") as csv_file:
        reader = csv.DictReader(csv_file, delimiter=";")
        transactions = [TinkoffTransaction.model_validate(row) for row in reader]
    return transactions
