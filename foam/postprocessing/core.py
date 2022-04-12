__all__ = ['VTK']


import typing as t
import warnings as w

from ..type import Path

if t.TYPE_CHECKING:
    import numpy as np
    import vtkmodules as vtk

    from ..core import Foam


class VTK:
    '''OpenFOAM VTK postprocessing'''

    Self = __qualname__

    def __init__(self, reader: 'vtk.vtkIOLegacy.vtkDataReader') -> None:
        self._points = self.to_numpy(reader.GetOutput().GetPoints().GetData())
        arrays = reader.GetOutput().GetPointData()
        self._fields = {}
        for ith in range(arrays.GetNumberOfArrays()):
            array = arrays.GetArray(ith)
            self._fields[array.GetName()] = self.to_numpy(array)
        reader.CloseVTKFile()

    def __getitem__(self, key: str) -> 'np.ndarray':
        return self._fields[key]

    @classmethod
    def from_unstructured_grid(cls, path: Path) -> Self:
        import vtkmodules.all as vtk

        reader = vtk.vtkUnstructuredGridReader()
        reader.SetFileName(str(path))
        reader.ReadAllFieldsOn()
        reader.ReadAllNormalsOn()
        reader.ReadAllScalarsOn()
        reader.ReadAllTCoordsOn()
        reader.ReadAllTensorsOn()
        reader.ReadAllVectorsOn()
        reader.Update()
        return cls(reader)

    @classmethod
    def from_foam(cls, foam: 'Foam', options: str = '', **kwargs) -> t.Iterator[Self]:
        kwargs['unsafe'] = True
        foam.cmd.run([f'foamToVTK {options}'], **kwargs)
        for path in (foam._dest/'VTK').iterdir():
            if path.is_file():
                yield cls.from_unstructured_grid(path)

    @property
    def points(self) -> 'np.ndarray':
        return self._points

    @property
    def fields(self) -> 'np.ndarray':
        return self._fields

    def keys(self) -> t.List[str]:
        return list(self._fields.keys())

    def centroid(self, key: str) -> 'np.ndarray':
        field = self.fields[key]
        if len(field.shape) != 1:
            w.warn('NotImplemented')
        return (self.points.T @ field) / sum(field)

    def to_numpy(self, array: 'vtk.vtkCommonCore.vtkDataArray') -> 'np.ndarray':
        from vtkmodules.util.numpy_support import vtk_to_numpy

        return vtk_to_numpy(array)
