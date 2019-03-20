import logging
from typing import TypeVar, Generic, Any, Type
from abc import ABCMeta, abstractmethod

logger = logging.getLogger(__name__)

TSelf = TypeVar('TSelf', bound='AbstractCacheMeta')
TK = TypeVar('TK')
TV = TypeVar('TV')


class AbstractCacheMeta(type, Generic[TK, TV], metaclass=ABCMeta):

    @abstractmethod
    def _getkey(self: TSelf, *args: Any, **kwargs: Any) -> TK:
        pass

    @abstractmethod
    def __getitem__(self: TSelf, key: TK) -> TV:
        pass

    @abstractmethod
    def __setitem__(self: TSelf, key: TK, value: TV) -> None:
        pass

    @abstractmethod
    def __contains__(self: TSelf, key: TK) -> bool:
        pass

    def __call__(self: TSelf, *args: Any, **kwargs: Any) -> TV:
        key = self._getkey(*args, **kwargs)
        if key in self:
            logger.debug('Cache hit')
            instance = self[key]
        else:
            logger.debug('Cache missed')
            instance = super().__call__(*args, **kwargs)
            self[key] = instance
        return instance
