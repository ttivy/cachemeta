import logging
from typing import TypeVar, Any, Union
import os
import pickle
import hashlib
from .abstract import AbstractCacheMeta

logger = logging.getLogger(__name__)

PathLike = Union[str, os.PathLike]
TSelf = TypeVar('TSelf', bound='PickleCacheMeta')
TV = TypeVar('TV')


class PickleCacheMeta(AbstractCacheMeta[PathLike, TV]):

    def _getkey(self: TSelf, *args: Any, **kwargs: Any) -> PathLike:
        hashable = tuple(args), tuple(kwargs.items())
        hex = hashlib.sha1(repr(hashable).encode()).hexdigest()
        return '%s.pickle' % hex

    def __getitem__(self: TSelf, path: PathLike) -> TV:
        with open(path, 'rb') as f:
            return pickle.load(f)

    def __setitem__(self: TSelf, path: PathLike, instance: TV) -> None:
        with open(path, 'wb') as f:
            pickle.dump(instance, f)

    def __contains__(self: TSelf, path: PathLike) -> bool:
        return os.path.isfile(path)
