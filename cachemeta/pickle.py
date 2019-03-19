import logging
from typing import TypeVar, Any, Callable, Hashable, Optional, Union
import os
import pickle
import hashlib
from .abstract import AbstractCacheMeta

logger = logging.getLogger(__name__)

PathLike = Union[str, os.PathLike]
TSelf = TypeVar('TSelf', bound='PickleCacheMeta')
TI = TypeVar('TI')


class PickleCacheMeta(AbstractCacheMeta[PathLike, TI]):

    def __init__(self: TSelf, name: str, bases: tuple, namespace: dict,
                 path: Optional[Callable[..., PathLike]] = None) -> None:
        if path is None:
            path = self.default_path
        super().__init__(name, bases, namespace, hash=path)

    def __getitem__(self: TSelf, path: PathLike) -> TI:
        with open(path, 'rb') as f:
            return pickle.load(f)

    def __setitem__(self: TSelf, path: PathLike, instance: TI) -> None:
        with open(path, 'wb') as f:
            pickle.dump(instance, f)

    def __contains__(self: TSelf, path: PathLike) -> bool:
        return os.path.isfile(path)

    @staticmethod
    def default_path(*args: Any, **kwargs: Any) -> PathLike:
        hashable = tuple(args), tuple(kwargs.items())
        hex = hashlib.sha1(repr(hashable).encode()).hexdigest()
        return '%s.pickle' % hex
