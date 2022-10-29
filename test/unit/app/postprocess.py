import pathlib as p
import shutil
import unittest

import numpy as np

from foam import Foam
from foam.util.decorator import suppress


class Test(unittest.TestCase):
    '''Test for PostProcess and VTK'''

    @classmethod
    @suppress.stderr.decorator_without_previous
    @suppress.stdout.decorator_without_previous
    def setUpClass(cls) -> None:
        cls._path = p.Path(__file__).parent / 'case'
        cls._foam = Foam.from_demo('cavity', verbose=False)
        cls._foam.save(cls._path)
        cls._foam.cmd.all_run(overwrite=False, exception=False)
        cls._foam.post.vtks_set(point=True, cell=True)

    @classmethod
    def tearDownClass(cls) -> None:
        shutil.rmtree(cls._foam.destination)

    @suppress.stdout.decorator_without_previous
    def test_postprocess_logs(self) -> None:
        for key, value in self._foam.post.logs.items():
            self.assertIsInstance(key, str)
            self.assertIsInstance(value, np.ndarray)
            self.assertEqual(len(value.shape), 2)

    @suppress.stderr.decorator_without_previous
    def test_postprocess_centroids(self) -> None:
        for key, values in self._foam.post.centroids(structured=False).items():
            self.assertIsInstance(key, str)
            for time, value in values.items():
                self.assertIsInstance(time, (float, int))
                self.assertIsInstance(value, np.ndarray)
                self.assertIn(len(value.shape), {1, 2})

    def test_postprocess_probe(self) -> None:
        location = (0.0, 0.0, 0.0)
        for key, values in self._foam.post.probe(location).items():
            self.assertIsInstance(key, str)
            for time, value in values.items():
                self.assertIsInstance(time, (float, int))
                if isinstance(value, np.number):
                    self.assertEqual(len(value.shape), 0)
                elif isinstance(value, np.ndarray):
                    self.assertEqual(len(value.shape), 1)
                else:
                    self.assertTrue(False)

    def test_vtk_points(self) -> None:
        for vtk in self._foam.post.vtks:
            self.assertIsInstance(vtk.points, np.ndarray)
            self.assertEqual(len(vtk.points.shape), 2)

    def test_vtk_cells(self) -> None:
        for vtk in self._foam.post.vtks:
            self.assertIsInstance(vtk.cells, np.ndarray)
            self.assertEqual(len(vtk.cells.shape), 2)

    def test_vtk_point_fields(self) -> None:
        for vtk in self._foam.post.vtks:
            for key, value in vtk.point_fields.items():
                self.assertIsInstance(key, str)
                self.assertIsInstance(value, np.ndarray)
                self.assertIn(len(value.shape), {1, 2})

    def test_vtk_cell_fields(self) -> None:
        for vtk in self._foam.post.vtks:
            for key, value in vtk.cell_fields.items():
                self.assertIsInstance(key, str)
                self.assertIsInstance(value, np.ndarray)
                self.assertIn(len(value.shape), {1, 2})
