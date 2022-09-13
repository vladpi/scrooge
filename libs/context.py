import abc
import logging

import pydantic

logger = logging.getLogger(__name__)


class ContextBase(pydantic.BaseModel, abc.ABC):
    class Config:  # noqa: WPS306, WPS431
        arbitrary_types_allowed = True
        allow_mutation = False

    async def close(self) -> None:
        try:
            logger.info('Closing context')
            await self._do_close()
        except Exception:
            logger.exception('Failed to close context')
            raise

    @abc.abstractmethod
    async def _do_close(self) -> None:
        raise NotImplementedError
