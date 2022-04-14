__all__ = ['VTK']


import collections as c
import functools as f
import typing as t
import warnings as w

from ..type import Path

if t.TYPE_CHECKING:
    import numpy as np
    import vtkmodules as vtk

    from ..core import Foam


class VTK:
    '''OpenFOAM VTK post-processing'''

    Self = __qualname__

    def __init__(self, reader: 'vtk.vtkIOLegacy.vtkDataReader') -> None:
        self._points = self._to_numpy(reader.GetOutput().GetPoints().GetData())
        arrays = reader.GetOutput().GetPointData()
        self._fields = {}
        for ith in range(arrays.GetNumberOfArrays()):
            array = arrays.GetArray(ith)
            self._fields[array.GetName()] = self._to_numpy(array)
        reader.CloseVTKFile()

    def __contains__(self, key: str) -> bool:
        return key in self._fields

    def __getitem__(self, key: str) -> 'np.ndarray':
        return self._fields[key]

    @classmethod
    def from_file(cls, path: Path) -> Self:
        import vtkmodules.all as vtk

        reader = vtk.vtkGenericDataObjectReader()
        reader.SetFileName(str(path))
        for attr in dir(reader):
            if attr.startswith('ReadAll') and attr.endswith('On'):
                getattr(reader, attr)()
        reader.Update()
        return cls(reader)

    @classmethod
    def from_foam(cls, foam: 'Foam', options: str = '', overwrite: bool = False) -> t.Iterator[Self]:
        foam.cmd.run([f'foamToVTK {options}'], overwrite=overwrite, exception=False, unsafe=True)
        paths = [
            path
            for path in (foam._dest/'VTK').iterdir()
            if path.is_file() and path.suffix=='.vtk'
        ]
        for path in sorted(paths, key=lambda p: int(p.stem.rsplit('_', maxsplit=1)[-1])):
            yield cls.from_file(path)

    @property
    def points(self) -> 'np.ndarray':
        return self._points

    @property
    def fields(self) -> 'np.ndarray':
        return self._fields

    @property
    def x(self) -> 'np.ndarray':
        return self._points[:, 0]

    @property
    def y(self) -> 'np.ndarray':
        return self._points[:, 1]

    @property
    def z(self) -> 'np.ndarray':
        return self._points[:, 2]

    def keys(self) -> t.List[str]:
        return list(self._fields.keys())

    @f.lru_cache
    def density(self, nx: int, ny: int, nz: int) -> 'np.ndarray':
        import numpy as np

        xs, ys, zs = self.points.T
        x0, xn = xs.min(), xs.max()
        y0, yn = ys.min(), ys.max()
        z0, zn = zs.min(), zs.max()
        dx, dy, dz = (xn-x0)/nx, (yn-y0)/ny, (zn-z0)/nz
        density = np.ones(self.points.shape[0])
        f = lambda ns, n0, dn, nn: np.clip(np.round((ns-n0)/dn-0.5).astype(np.uint64), 0, nn-1)
        iths, jths, kths = f(xs, x0, dx, nx), f(ys, y0, dy, ny), f(zs, z0, dz, nz)
        count = c.Counter(zip(iths, jths, kths))
        for nth, (ith, jth, kth) in enumerate(zip(iths, jths, kths)):
            density[nth] /= count[(ith, jth, kth)]
        return density

    def centroid(self, key: str, density: t.Optional['np.ndarray'] = None) -> 'np.ndarray':
        '''
        - Argument:
            - density: this parameter must be specified for unstructured grid
        '''
        field = self.fields[key]
        density = 1.0 if density is None else density
        if len(field.shape) != 1:
            w.warn('NotImplemented')
        return (self.points.T @ (field*density)) / sum(field*density)

    def centroid_with_density(self, key: str, nx: int, ny: int, nz: int) -> 'np.ndarray':
        return self.centroid(key, self.density(nx, ny, nz))

    def _to_numpy(self, array: 'vtk.vtkCommonCore.vtkDataArray') -> 'np.ndarray':
        from vtkmodules.util.numpy_support import vtk_to_numpy

        return vtk_to_numpy(array)
