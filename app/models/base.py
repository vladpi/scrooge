import abc
from datetime import datetime
from typing import Union
from uuid import UUID

import pydantic

AllowedIdType = Union[int, str]


class BaseIdentity(abc.ABC):  # noqa: B024
    """Models' identity type.

    This class is a helper that forces writing code with explicit specification of
    identities. When creating new model, create special identity class for it
    like this::

        class ModelId(Identity):
            pass

        class Model(BaseModel):
            id: ModelId

    This setup would benefit from static analyzer.
    """


class IntIdentity(BaseIdentity, int):  # noqa: WPS600
    """Int Identity"""


class StrIdentity(BaseIdentity, str):  # noqa: WPS600
    """Str Identity"""


class UUIDIdentity(BaseIdentity, UUID):  # noqa: WPS600
    """UUID Identity"""


class BaseModel(pydantic.BaseModel):
    created_at: datetime
    updated_at: datetime


class BaseCreateRequest(pydantic.BaseModel):
    """Base Create Request"""


class BaseUpdateRequest(pydantic.BaseModel):
    """Base Update Request"""
