__all__ = ['Test']


import unittest

from foam.parse.case import Case


class Test(unittest.TestCase):
    '''Test for Case'''

    @classmethod
    def setUpClass(cls) -> None:
        cls._case = Case.default()

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_data(self) -> None:
        data = {
            'dict': {
                'a': [True, False],
                'b': 1,
                'c': 3.14,
                'd': 'e',
                'f': {'g': {'h': {'i': 'j'}}},
                'k': ['l', 'm', 'n'],
            },
            'list-1': [
                {'a': None, 'b': 'c'},
                {'d': None, 'e': 'f'},
            ],
            'list-2': [
                {'a, b': 'c', 'd|e': 'f'},
                {'(g)': 'h', 'i.*': 'j k'},
            ],
        }
        self.assertListEqual(
            list(self._case.data(data)), [
                'dict {a (True False); b 1; c 3.14; d e; f {g {h {i j;}}} k (l m n);}',
                'list-1 (a {b c;} d {e f;});',
                'list-2 ({a,b c; "d|e" f;} {"(g)" h; "i.*" j k;});',
            ],
        )
