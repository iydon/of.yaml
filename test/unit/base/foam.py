import pathlib as p
import shutil
import unittest

from foam import Foam


class Test(unittest.TestCase):
    '''Test for Command

    TODO:
        - Foam.from_openfoam
    '''

    @classmethod
    def setUpClass(cls) -> None:
        cls._path = p.Path(__file__).parent / 'case'
        cls._foam = Foam.from_demo('cavity', verbose=False)

    @classmethod
    def tearDownClass(cls) -> None:
        shutil.rmtree(cls._path, ignore_errors=True)

    def test_from_demos(self) -> None:
        foams = Foam.from_demos(verbose=False)
        self.assertGreater(len(foams), 0)

    def test_from_remote_demos(self) -> None:
        foams = Foam.from_remote_demos(timeout=7.0, verbose=False)
        self.assertGreater(len(foams), 0)

    def test_data_meta(self) -> None:
        self.assertTrue(self._foam.data.is_list())
        self.assertTrue(self._foam.meta.is_dict())

    def test_cmd_info_post(self) -> None:
        self._foam.reset()
        with self.assertRaises(AssertionError):
            self._foam.cmd
        self._foam.save(self._path)
        self._foam.cmd
        self._foam.info
        self._foam.post

    def test_cached_property(self) -> None:
        self.assertIsInstance(self._foam.application, str)
        self.assertIsInstance(self._foam.number_of_processors, int)
        self.assertIsInstance(self._foam.pipeline, list)
        self.assertGreater(len(self._foam.pipeline), 0)
        self.assertIsInstance(self._foam.fields, set)
        self.assertTrue(all(isinstance(field, str) for field in self._foam.fields))
        if self._foam.ndim is not None:
            self.assertIsInstance(self._foam.ndim, int)

    def test_environ(self) -> None:
        for key, value in self._foam.environ.items():
            self.assertTrue(key.isupper())
            self.assertIsInstance(value, str)

    def test_copy(self) -> None:
        self.assertIsNot(self._foam, self._foam.copy())
