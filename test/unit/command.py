import pathlib as p
import shutil
import unittest

import foam


class Test(unittest.TestCase):
    '''Test demo'''

    @classmethod
    def setUpClass(cls) -> None:
        cls._root = p.Path(__file__).parent
        cls._foam = foam.Foam.from_demo('cavity')
        cls._foam.save(cls._root/'case')

    @classmethod
    def tearDownClass(cls) -> None:
        shutil.rmtree(cls._foam.destination)

    def test_macros(self) -> None:
        for key, val in self._foam.cmd.macros.items():
            self.assertIn('__', key)
            self.assertIsInstance(val, str)

    def test_allrun(self) -> None:
        # 1
        codes = self._foam.cmd.all_run(overwrite=True, exception=False)
        self.assertEqual(sum(codes), 0)
        self.assertEqual(len(codes), len(self._foam.pipeline))
        self.assertEqual(len(codes), len(self._foam.cmd.logs))
        self.assertEqual(min(self._foam.cmd.times), self._foam['foam']['system', 'controlDict', 'startTime'])
        self.assertEqual(max(self._foam.cmd.times), self._foam['foam']['system', 'controlDict', 'endTime'])
        # 2
        codes = self._foam.cmd.all_run(overwrite=False, exception=False)
        self.assertSetEqual(set(codes), {-1})
        # 3
        with self.assertRaises(Exception):
            self._foam.cmd.all_run(overwrite=False, exception=True)

    def test_allclean(self) -> None:
        self._foam.cmd.all_clean()
        self.assertSetEqual(self._foam.cmd.logs, set())
        self.assertListEqual(self._foam.cmd.times, [self._foam['foam']['system', 'controlDict', 'startTime']])

    def test_raw_pwd(self) -> None:
        cp = self._foam.cmd.raw('pwd')
        self.assertEqual(cp.returncode, 0)
        self.assertEqual(cp.stderr.strip().decode(), '')
        self.assertEqual(cp.stdout.strip().decode(), self._foam.destination.as_posix())
