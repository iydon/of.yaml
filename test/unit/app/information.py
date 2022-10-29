import pathlib as p
import shutil
import unittest

from foam import Foam


class Test(unittest.TestCase):
    '''Test for Information'''

    @classmethod
    def setUpClass(cls) -> None:
        cls._root = p.Path(__file__).parent
        cls._foam = Foam.from_demo('cavity', verbose=False)
        cls._foam.save(cls._root/'case')

    @classmethod
    def tearDownClass(cls) -> None:
        shutil.rmtree(cls._foam.destination)

    def test_cmd(self) -> None:
        self.assertIsNotNone(self._foam.info.cmd)

    def test_environ(self) -> None:
        for key, value in self._foam.info.environ.items():
            self.assertTrue(key.isupper())
            self.assertIsInstance(value, str)

    def test_root(self) -> None:
        self.assertTrue(self._foam.info.root.exists())

    def test_shared_libraries(self) -> None:
        self.assertTrue(all(p.Path(path).exists() for path in self._foam.info.shared_libraries))

    def test_search(self) -> None:
        results = self._foam.info.search('fvSchemes', 'divSchemes', 'div(rhoPhi, U)')
        self.assertIsInstance(results, set)
        self.assertTrue(all(isinstance(result, str) for result in results))

    def test_search_yaml(self) -> None:
        results = self._foam.info.search_yaml('fvSchemes', 'divSchemes', 'div(rhoPhi, U)')
        for key, values in results.items():
            self.assertIsInstance(key, str)
            self.assertIsInstance(values, set)
            self.assertTrue(all(isinstance(value, str) for value in values))

    def test_commands(self) -> None:
        results = self._foam.info.commands()
        self.assertIsInstance(results, set)
        self.assertTrue(all(isinstance(result, str) for result in results))
