import abc
from typing import Any, Generic, Type, TypeVar

from app.db.base import DbModelBase
from app.models.base import BaseModel

_Model = TypeVar('_Model', bound=BaseModel)
_DbModel = TypeVar('_DbModel', bound=DbModelBase)


class MapperBase(abc.ABC, Generic[_Model, _DbModel]):
    __model__: Type[_Model]
    __db_model__: Type[_DbModel]
    __id_name__: str = 'id'

    @abc.abstractmethod
    def parse(self, row: Any) -> _Model:
        raise NotImplementedError
