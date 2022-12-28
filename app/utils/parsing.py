import re
from datetime import date

import dateparser


def parse_amount_and_comment(text: str | None) -> tuple[str | None, str | None]:
    if text is None:
        return None, None

    amount = parse_amount(text)
    comment = text.replace(amount, '').strip() if amount is not None else None

    return amount, comment


def parse_amount(text: str) -> str | None:
    pattern = r'(\d+[\.\,]?\d*)'
    regexp_result = re.search(pattern, text)

    if regexp_result is not None:
        return regexp_result.group(0).replace(',', '.')

    return None


def parse_date(text: str | None) -> date | None:
    if text is None:
        return None
    parsed_datetime = dateparser.parse(text, languages=['ru'])
    return parsed_datetime.date() if parsed_datetime is not None else None
