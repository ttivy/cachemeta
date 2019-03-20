## About
Python metaclass for cache instance

## Installation
```Shell
pip install git+https://github.com/ttivy/cachemeta
```

## Examples

#### Cached instance

```Python
from cachemeta import DictCacheMeta

class CachedDict(dict, metaclass=DictCacheMeta):
    def __init__(self, *args, **kwargs):
        print('__init__', args, kwargs)
        super().__init__(*args, **kwargs)

# The same object if created from the same args
x = CachedDict(a=1, b=2)
y = CachedDict(a=1, b=2, c=3)
z = CachedDict(a=1, b=2, c=3)
# __init__ () {'a': 1, 'b': 2}
# __init__ () {'a': 1, 'b': 2, 'c': 3}

# z is cached y
assert id(x) != id(y)
assert id(y) == id(z)
```

#### Key customization

```Python
from cachemeta import DictCacheMeta

class CachedObject(metaclass=DictCacheMeta):
    def __init__(self, *args, **kwargs):
        print('__init__', args, kwargs)
        super().__init__()
        self.args, self.kwargs = args, kwargs

    # Customized cache key
    @classmethod
    def _getkey(cls, *args, **kwargs):
        if len(args) > 0:
            return args[0]
        return None

# The same object if created from the same first args
x = CachedObject(1, 2)
y = CachedObject(1, 2, 3)
z = CachedObject(4, 5, 6)
# __init__ (1, 2) {}
# __init__ (4, 5, 6) {}

# y is cached x
assert id(x) == id(y)
assert id(y) != id(z)
```

#### Cache to pickle

```Python
import os
from cachemeta import PickleCacheMeta

CACHE_DIR = './cache'

# Make cache dir
if not os.path.isdir(CACHE_DIR):
    os.mkdir(CACHE_DIR)

class PickledObject(metaclass=PickleCacheMeta):
    def __init__(self, *args, **kwargs):
        print('__init__', args, kwargs)
        super().__init__()
        self.args, self.kwargs = args, kwargs

    # Customized cache path
    @classmethod
    def _getkey(cls, number, *args, **kwargs):
        # Filename is lower 3 digits in hex
        filename = ('%03x' % number)[-3:] + '.pickle'
        return os.path.join(CACHE_DIR, filename)

# The same object if created from
# the same lower 3 digits in hex of first args
x = PickledObject(0x000, 1)
y = PickledObject(0x001, 2)
z = PickledObject(0x1000, 3)
# __init__ (0, 1) {}
# __init__ (1, 2) {}

# z is pickled x, but different instances
assert id(x) != id(y) != id(z)
assert (x.args, x.kwargs) == (z.args, z.kwargs)
```
