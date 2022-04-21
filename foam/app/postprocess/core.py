__all__ = ['PostProcess', 'VTK']


import typing as t
import warnings as w

from ...base import Foam, Array, Path

if t.TYPE_CHECKING:
    import vtkmodules as vtk


class PostProcess:
    '''OpenFOAM post-processing'''

    Self = __qualname__

    def __init__(self, foam: Foam) -> None:
        self._foam = foam
        self._vtks = None

    @classmethod
    def from_foam(cls, foam: Foam) -> Self:
        return cls(foam)

    @property
    def vtks(self) -> t.List['VTK']:
        if self._vtks is None:
            self._vtks = list(VTK.from_foam(self._foam))
        return self._vtks


class VTK:
    '''OpenFOAM VTK post-processing'''

    Self = __qualname__

    def __init__(
        self,
        reader: 'vtk.vtkIOLegacy.vtkDataReader',
        foam: t.Optional[Foam] = None, point: bool = True, cell: bool = True,
    ) -> None:
        self._foam = foam
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

    def __getitem__(self, key: str) -> None:
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
    def from_foam(
        cls,
        foam: Foam, options: str = '', overwrite: bool = False,
        **kwargs,
    ) -> t.Iterator[Self]:
        assert foam._dest is not None, 'Please call `Foam::save` method first'

        foam.cmd.run(['postProcess -func writeCellCentres'], overwrite=True, exception=False, unsafe=True)
        foam.cmd.run(['postProcess -func writeCellVolumes'], overwrite=True, exception=False, unsafe=True)
        foam.cmd.run([f'foamToVTK {options}'], overwrite=overwrite, exception=False, unsafe=True)
        paths = [
            path
            for path in (foam._dest/'VTK').iterdir()
            if path.is_file() and path.suffix=='.vtk'
        ]
        for path in sorted(paths, key=lambda p: int(p.stem.rsplit('_', maxsplit=1)[-1])):
            yield cls.from_file(path, foam=foam, **kwargs)

    @property
    def points(self) -> Array('2D'):
        assert self._points is not None

        return self._points

    @property
    def cells(self) -> Array('2D'):
        assert self._cells is not None

        return self._cells

    @property
    def point_fields(self) -> t.Dict[str, Array('12D')]:
        assert self._point_fields is not None

        return self._point_fields

    @property
    def cell_fields(self) -> t.Dict[str, Array('12D')]:
        assert self._cell_fields is not None

        return self._cell_fields

    @property
    def x(self) -> Array('1D'):
        return self.points[:, 0]

    @property
    def y(self) -> Array('1D'):
        return self.points[:, 1]

    @property
    def z(self) -> Array('1D'):
        return self.points[:, 2]

    def keys(self) -> None:
        raise NotImplementedError

    def centroid(self, key: str, structured: bool = False) -> Array('12D'):
        if structured:
            coords = self._points
            field = self._point_fields[key]
        else:
            coords = self._cells
            if self._cell_fields[key].ndim == 1:
                weights = self._cell_fields['V']
            else:  # ndim == 2
                weights = self._cell_fields['V'][:, None]
            field = self._cell_fields[key] * weights
        if field.ndim != 1:
            w.warn(f'NotImplemented: {key}')
        return (coords.T @ field) / sum(field)

    def centroids(
        self,
        keys: t.Optional[t.Set[str]] = None, structured: bool = False,
    ) -> t.Dict[str, Array('12D')]:
        return {
            key: self.centroid(key, structured)
            for key in (keys or self._foam.fields)
        }

    def centroid_with_args(self, *keys: str, structured: bool = False) -> t.Dict[str, Array('12D')]:
        return self.centroids(set(keys), structured=structured)

    def probe(
        self,
        location: t.Tuple[float, float, float], keys: t.Optional[t.Set[str]] = None,
        point: bool = True, func: t.Optional[t.Callable] = None,
    ) -> t.Dict[str, Array('01D')]:
        location = tuple(map(float, location))
        return self.probes(location, keys=keys, point=point, func=func)[location]

    def probes(
        self,
        *locations: t.Tuple[float, float, float],
        keys: t.Optional[t.Set[str]] = None, point: bool = True, func: t.Optional[t.Callable] = None,
    ) -> t.Dict[t.Tuple[float, float, float], t.Dict[str, Array('01D')]]:
        '''
        - Reference:
            - https://github.com/OpenFOAM/OpenFOAM-7/tree/master/src/sampling/probes
        '''
        assert self._foam is not None

        import numpy as np

        keys = keys or self._foam.fields
        coords = self.points if point else self.cells
        fields = self.point_fields if point else self.cell_fields
        func = func or (lambda x: np.square(x).mean(axis=1))
        ans = {}
        for location in locations:
            index = np.argmin(func(coords-location))
            ans[tuple(map(float, location))] = {
                key: fields[key][index]
                for key in keys
            }
        return ans

    def _to_numpy(self, array: 'vtk.vtkCommonCore.vtkDataArray') -> Array('12D'):
        from vtkmodules.util.numpy_support import vtk_to_numpy

        return vtk_to_numpy(array)
