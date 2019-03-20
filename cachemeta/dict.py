import logging
from typing import TypeVar, Any, Hashable
from .abstract import AbstractCacheMeta

logger = logging.getLogger(__name__)

TSelf = TypeVar('TSelf', bound='DictCacheMeta')
TV = TypeVar('TV')


class DictCacheMeta(AbstractCacheMeta[Hashable, TV]):

    def __init__(self: TSelf, name: str, bases: tuple, namespace: dict
                 ) -> None:
        super().__init__(name, bases, namespace)
        self._cache: dict = dict()

    def _getkey(self: TSelf, *args: Any, **kwargs: Any) -> Hashable:
        return tuple(args), tuple(kwargs.items())

    def __getitem__(self: TSelf, key: Hashable) -> TV:
        return self._cache[key]

    def __setitem__(self: TSelf, key: Hashable, instance: object) -> None:
        self._cache[key] = instance

    def __contains__(self: TSelf, key: Hashable) -> bool:
        return key in self._cache
