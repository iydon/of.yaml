__all__ = ['VTK']


import collections as c
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

    def __init__(self, reader: 'vtk.vtkIOLegacy.vtkDataReader', point: bool = True, cell: bool = True) -> None:
        import numpy as np

        self._points, self._cells = None, None
        self._point_fields = {}
        self._cell_fields = {}
        if point:
            self._points = self._to_numpy(reader.GetOutput().GetPoints().GetData())
            arrays = reader.GetOutput().GetPointData()
            for ith in range(arrays.GetNumberOfArrays()):
                array = arrays.GetArray(ith)
                self._point_fields[array.GetName()] = self._to_numpy(array)
        if cell:
            arrays = reader.GetOutput().GetCellData()
            for ith in range(arrays.GetNumberOfArrays()):
                array = arrays.GetArray(ith)
                self._cell_fields[array.GetName()] = self._to_numpy(array)
            cell_ids = set(self._cell_fields['cellID'])  # TODO: explore why cell_id is sometimes repeated
            for key, value in self._cell_fields.items():
                self._cell_fields[key] = value[:len(cell_ids)]
            self._cells = self._cell_fields['C']
        reader.CloseVTKFile()

    def __contains__(self, key: str) -> bool:
        return key in self._point_fields or key in self._cell_fields

    def __getitem__(self, key: str) -> 'np.ndarray':
        raise NotImplementedError

    @classmethod
    def from_file(cls, path: Path, **kwargs) -> Self:
        import vtkmodules.all as vtk

        reader = vtk.vtkGenericDataObjectReader()
        reader.SetFileName(str(path))
        for attr in dir(reader):
            if attr.startswith('ReadAll') and attr.endswith('On'):
                getattr(reader, attr)()
        reader.Update()
        return cls(reader, **kwargs)

    @classmethod
    def from_foam(cls, foam: 'Foam', options: str = '', overwrite: bool = False, **kwargs) -> t.Iterator[Self]:
        foam.cmd.run(['postProcess -func writeCellCentres'], overwrite=True, exception=False, unsafe=True)
        foam.cmd.run(['postProcess -func writeCellVolumes'], overwrite=True, exception=False, unsafe=True)
        foam.cmd.run([f'foamToVTK {options}'], overwrite=overwrite, exception=False, unsafe=True)
        paths = [
            path
            for path in (foam._dest/'VTK').iterdir()
            if path.is_file() and path.suffix=='.vtk'
        ]
        for path in sorted(paths, key=lambda p: int(p.stem.rsplit('_', maxsplit=1)[-1])):
            yield cls.from_file(path, **kwargs)

    @property
    def points(self) -> 'np.ndarray':
        assert self._points
        return self._points

    @property
    def cells(self) -> 'np.ndarray':
        assert self._cells
        return self._cells

    @property
    def point_fields(self) -> t.Dict[str, 'np.ndarray']:
        assert self._point_fields
        return self._point_fields

    @property
    def cell_fields(self) -> t.Dict[str, 'np.ndarray']:
        assert self._cell_fields
        return self._cell_fields

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
        raise NotImplementedError

    def centroid(self, key: str, structured: bool = False) -> 'np.ndarray':
        if structured:
            coords = self._points
            field = self._point_fields[key]
        else:
            coords = self._cells
            field = self._cell_fields[key] * self._cell_fields['V']
        if len(field.shape) != 1:
            w.warn('NotImplemented')
        return (coords.T @ field) / sum(field)

    def _to_numpy(self, array: 'vtk.vtkCommonCore.vtkDataArray') -> 'np.ndarray':
        from vtkmodules.util.numpy_support import vtk_to_numpy

        return vtk_to_numpy(array)
