import unittest
from unittest import mock
import os
import glob
from cachemeta import PickleCacheMeta


class Cache(metaclass=PickleCacheMeta):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def __eq__(self, other):
        if type(self) is type(other):
            return self.args == other.args and self.kwargs == other.kwargs
        return False


class TestPickle(unittest.TestCase):
    TEMP_DIR = './_temp'

    @classmethod
    def setUpClass(cls):
        if not os.path.isdir(cls.TEMP_DIR):
            os.mkdir(cls.TEMP_DIR)
        os.chdir(cls.TEMP_DIR)

    @classmethod
    def tearDownClass(cls):
        os.chdir('..')
        os.rmdir(cls.TEMP_DIR)

    def tearDown(self):
        for cache_file in glob.glob('*.pickle'):
            os.remove(cache_file)

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
