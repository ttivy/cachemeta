import unittest
from cachemeta import DictCacheMeta


class Cache(metaclass=DictCacheMeta):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs


class TestCache(unittest.TestCase):

    def test_cache_blank(self):
        c = Cache()
        c_ = Cache()
        self.assertEqual(c, c_)

    def test_cache_args(self):
        c1 = Cache(1)
        c1_ = Cache(1)
        c2 = Cache(2)
        self.assertEqual(c1, c1_)
        self.assertNotEqual(c1, c2)

    def test_cache_kwargs(self):
        ca = Cache(a=1)
        ca_ = Cache(a=1)
        cb = Cache(b=1)
        self.assertEqual(ca, ca_)
        self.assertNotEqual(ca, cb)

    def test_cache(self):
        ca = Cache(('a', 1))
        ca_ = Cache(a=1)
        self.assertNotEqual(ca, ca_)


if __name__ == '__main__':
    unittest.main()
