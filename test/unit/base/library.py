__all__ = ['Test']


import sys
import unittest

from foam.base import lib


class Test(unittest.TestCase):
    '''Test for Library'''

    def test_lazy_import(self) -> None:
        number_0 = len(sys.modules)
        for attr in lib.__all__:
            getattr(lib, attr)
        number_1 = len(sys.modules)
        for attr in lib.__all__:
            load = getattr(getattr(lib, attr), '_', None)
            if load is not None:
                load()
        number_2 = len(sys.modules)
        self.assertEqual(number_0, number_1)
        self.assertLess(number_1, number_2)
