import csv
import pathlib

from .schemas import Account, Category, Transaction


def parse_csv_dump(dump_filename: str | pathlib.Path) -> list[Transaction]:
    transactions: list[Transaction] = []

    with open(dump_filename, 'r') as dump_file:
        # Skip first 3 lines of file, because it contains service info
        for _ in range(3):
            next(dump_file)

        reader = csv.DictReader(dump_file)
        for row in reader:
            transactions.append(_parse_transaction_row(row))

    return transactions


def _parse_transaction_row(row: dict[str, str]) -> Transaction:
    income_account = None
    if row['incomeAccountName']:
        income_account = Account(
            name=row['incomeAccountName'],
            currency=row['incomeCurrencyShortTitle'],
        )

    outcome_account = None
    if row['outcomeAccountName']:
        outcome_account = Account(
            name=row['outcomeAccountName'],
            currency=row['outcomeCurrencyShortTitle'],
        )

    return Transaction(
        at_date=row['date'],
        category=Category(name=row['categoryName']),
        comment=row['comment'],
        income=row['income'].replace(',', '.') or None,
        income_account=income_account,
        outcome=row['outcome'].replace(',', '.') or None,
        outcome_account=outcome_account,
        created_at=row['createdDate'],
        updated_at=row['changedDate'],
    )
