from typing import Any, Optional

from pydantic import PostgresDsn


class SQLAlchemyPostgresDsn(PostgresDsn):
    def __new__(cls, url: Optional[str], **kwargs: Any) -> 'SQLAlchemyPostgresDsn':
        if url and url.startswith('postgres://'):
            url = url.replace('postgres://', 'postgresql://')

        if kwargs.get('scheme') == 'postgres':
            kwargs['scheme'] = 'postgresql'

        return super().__new__(cls, url, **kwargs)
