import abc
from typing import Any, Generic, Mapping, Type, TypeVar

from app.db.base import DbModelProto
from app.models.base import (
    BaseCreateRequest,
    BaseIdentity,
    BaseModel,
    BaseUpdateRequest,
)

_Model = TypeVar('_Model', bound=BaseModel)
_ModelCreate = TypeVar('_ModelCreate', bound=BaseCreateRequest)
_ModelUpdate = TypeVar('_ModelUpdate', bound=BaseUpdateRequest)
_ModelId = TypeVar('_ModelId', bound=BaseIdentity)

_DbModel = TypeVar('_DbModel', bound=DbModelProto)


class RepositoryBase(abc.ABC, Generic[_Model, _ModelId, _ModelCreate, _ModelUpdate]):
    @abc.abstractmethod
    async def create(self, create_model: _ModelCreate) -> _Model:
        """
        Raises:
            exceptions.RepositoryError:
            exceptions.CreateError:
            exceptions.DuplicateError:
        """
        raise NotImplementedError

    @abc.abstractmethod
    async def get(self, id_: _ModelId) -> _Model:
        """
        Raises:
            exceptions.RepositoryError:
            exceptions.NotFound:
        """
        raise NotImplementedError

    @abc.abstractmethod
    async def update(self, id_: _ModelId, update_model: _ModelUpdate) -> _Model:
        """
        Raises:
            exceptions.RepositoryError:
            exceptions.CreateError:
            exceptions.DuplicateError:
        """
        raise NotImplementedError

    @abc.abstractmethod
    async def delete(self, id_: _ModelId) -> None:
        """
        Raises:
            exceptions.RepositoryError:
            exceptions.NotFound:
        """
        raise NotImplementedError


class MapperBase(abc.ABC, Generic[_Model, _DbModel]):
    __model__: Type[_Model]
    __db_model__: Type[_DbModel]
    __id_name__: str = 'id'

    @abc.abstractmethod
    def parse(self, row: Mapping[str, Any]) -> _Model | None:
        raise NotImplementedError
