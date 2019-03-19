import logging
from typing import TypeVar, Any, Callable, Hashable, Optional
from .abstract import AbstractCacheMeta

logger = logging.getLogger(__name__)

TSelf = TypeVar('TSelf', bound='DictCacheMeta')
TI = TypeVar('TI')


class DictCacheMeta(AbstractCacheMeta[Hashable, TI]):

    def __init__(self: TSelf, name: str, bases: tuple, namespace: dict,
                 key: Optional[Callable[..., Hashable]] = None) -> None:
        if key is None:
            key = self.default_key
        super().__init__(name, bases, namespace, hash=key)
        self._cache: dict = dict()

    def __getitem__(self: TSelf, key: Hashable) -> TI:
        return self._cache[key]

    def __setitem__(self: TSelf, key: Hashable, instance: object) -> None:
        self._cache[key] = instance

    def __contains__(self: TSelf, key: Hashable) -> bool:
        return key in self._cache

    @staticmethod
    def default_key(*args: Any, **kwargs: Any) -> Hashable:
        return tuple(args), tuple(kwargs.items())
