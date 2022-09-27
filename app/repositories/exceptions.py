from typing import Optional, Union


class RepositoryError(Exception):
    """Base repository error"""


class NotFoundError(RepositoryError):
    """Not found repository error"""


class CreateError(RepositoryError):
    """Create repository error"""


class DuplicateError(RepositoryError):
    """Duplicate repository error"""


class UpdateError(RepositoryError):
    """Update repository error"""


class MappingError(RepositoryError):
    msg = "model wasn't properly mapped from DB"

    def __init__(self, msg: Optional[Union[str, Exception]] = None) -> None:
        super().__init__(msg or self.msg)
