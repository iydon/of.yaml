__all__ = ['Test']


import unittest

from foam.parse.case import Case


class Test(unittest.TestCase):
    '''Test for Case'''

    def test_example(self) -> None:
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
            list(Case.default().data(data)), [
                'dict {a (True False); b 1; c 3.14; d e; f {g {h {i j;}}} k (l m n);}',
                'list-1 (a {b c;} d {e f;});',
                'list-2 ({a,b c; "d|e" f;} {"(g)" h; "i.*" j k;});',
            ],
        )
