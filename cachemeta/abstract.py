import logging
from typing import TypeVar, Generic, Any, Type, Callable
from abc import ABCMeta, abstractmethod

logger = logging.getLogger(__name__)

TSelf = TypeVar('TSelf', bound='AbstractCacheMeta')
TH = TypeVar('TH')
TI = TypeVar('TI')


class AbstractCacheMeta(type, Generic[TH, TI], metaclass=ABCMeta):

    def __new__(cls: Type[TSelf], name: str, bases: tuple, namespace: dict,
                **kwargs: Any) -> type:
        return super().__new__(cls, name, bases, namespace)

    def __init__(self: TSelf, name: str, bases: tuple, namespace: dict,
                 hash: Callable[..., TH]) -> None:
        super().__init__(name, bases, namespace)
        self._hash = hash

    @abstractmethod
    def __getitem__(self: TSelf, hash: TH) -> TI:
        pass

    @abstractmethod
    def __setitem__(self: TSelf, hash: TH, instance: TI) -> None:
        pass

    @abstractmethod
    def __contains__(self: TSelf, hash: TH) -> bool:
        pass

    def __call__(self: TSelf, *args: Any, **kwargs: Any) -> TI:
        hash = self._hash(*args, **kwargs)
        if hash in self:
            logger.debug('Cache hit')
            instance = self[hash]
        else:
            logger.debug('Cache missed')
            instance = super().__call__(*args, **kwargs)
            self[hash] = instance
        return instance
