__all__ = ['PostProcess', 'VTK']


import typing as t
import warnings as w

from ...base import Foam, Array, Path, lib

if t.TYPE_CHECKING:
    import vtkmodules as vtk


class PostProcess:
    '''OpenFOAM post-processing'''

    def __init__(self, foam: Foam) -> None:
        self._foam = foam
        self._vtks = None
        self._logs = None

    @classmethod
    def from_foam(cls, foam: Foam) -> t.Self:
        return cls(foam)

    @property
    def vtks(self) -> t.List['VTK']:
        if self._vtks is None:
            self._vtks = list(VTK.from_foam(self._foam))
        return self._vtks

    @property
    def logs(self) -> t.Dict[str, t.Any]:
        '''Script extract data for each time-step from a log file for graphing

        - Reference:
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/bin/foamLog
        '''
        if self._logs is None:
            filename = next(log for log in self._foam.cmd.logs if self._foam.application in log.name).name
            self._foam.cmd.run([f'foamLog {filename}'], overwrite=True, exception=False, unsafe=True)
            self._logs = {
                path.name.replace('_0', ''): lib['numpy'].loadtxt(path)
                for path in (self._foam._dest/'logs').iterdir()
                if path.suffix != '.awk'
            }
        return self._logs

    def vtks_set(self, **kwargs) -> t.List['VTK']:
        self._vtks = list(VTK.from_foam(self._foam, **kwargs))
        return self._vtks

    def centroid(self, key: str, structured: bool = False) -> t.Dict[float, Array[1, 2]]:
        ans = {}
        for time, vtk in zip(self._foam.cmd.times, self.vtks):
            ans[time] = vtk.centroid(key, structured)
        return ans

    def centroids(
        self,
        keys: t.Optional[t.Set[str]] = None, structured: bool = False,
    ) -> t.Dict[str, t.Dict[float, Array[1, 2]]]:
        return {
            key: self.centroid(key, structured)
            for key in (keys or self._foam.fields)
        }

    def probe(
        self,
        location: t.Tuple[float, float, float], keys: t.Optional[t.Set[str]] = None,
        point: bool = True, func: t.Optional[t.Callable] = None,
    ) -> t.Dict[str, t.Dict[float, Array[0, 1]]]:
        location = tuple(map(float, location))
        return self.probes(location, keys=keys, point=point, func=func)[location]

    def probes(
        self,
        *locations: t.Tuple[float, float, float],
        keys: t.Optional[t.Set[str]] = None, point: bool = True, func: t.Optional[t.Callable] = None,
    ) -> t.Dict[t.Tuple[float, float, float], t.Dict[str, t.Dict[float, Array[0, 1]]]]:
        ans = {}
        for time, vtk in zip(self._foam.cmd.times, self.vtks):
            probes = vtk.probes(*locations, keys=keys, point=point, func=func)
            for location, probe in probes.items():
                for key, value in probe.items():
                    ans \
                        .setdefault(location, {}) \
                        .setdefault(key, {}) \
                        .setdefault(time, value)
        return ans


class VTK:
    '''OpenFOAM VTK post-processing'''

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
    def from_file(cls, path: Path, **kwargs) -> t.Self:
        assert lib['vtk'] is not None, 'pip install ifoam[vtk]'  # TODO: improve error message

        reader = lib['vtk'].vtkGenericDataObjectReader()
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
    ) -> t.Iterator[t.Self]:
        assert foam._dest is not None, 'Please call `Foam::save` method first'

        for name in ['writeCellCentres', 'writeCellVolumes']:
            foam.cmd.run([f'postProcess -func {name}'], suffix=f'.{name}', overwrite=overwrite, exception=False, unsafe=True)
        foam.cmd.run([f'foamToVTK {options}'], overwrite=overwrite, exception=False, unsafe=True)
        paths = [
            path
            for path in (foam._dest/'VTK').iterdir()
            if path.is_file() and path.suffix=='.vtk'
        ]
        for path in sorted(paths, key=lambda p: int(p.stem.rsplit('_', maxsplit=1)[-1])):
            yield cls.from_file(path, foam=foam, **kwargs)

    @property
    def points(self) -> Array[2]:
        assert self._points is not None

        return self._points

    @property
    def cells(self) -> Array[2]:
        assert self._cells is not None

        return self._cells

    @property
    def point_fields(self) -> t.Dict[str, Array[1, 2]]:
        assert self._point_fields is not None

        return self._point_fields

    @property
    def cell_fields(self) -> t.Dict[str, Array[1, 2]]:
        assert self._cell_fields is not None

        return self._cell_fields

    @property
    def x(self) -> Array[1]:
        return self.points[:, 0]

    @property
    def y(self) -> Array[1]:
        return self.points[:, 1]

    @property
    def z(self) -> Array[1]:
        return self.points[:, 2]

    def keys(self) -> None:
        raise NotImplementedError

    def centroid(self, key: str, structured: bool = False) -> Array[1, 2]:
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
            w.warn(f'Array2D is not yet guaranteed: {key}')
        return (coords.T @ field) / sum(field)

    def centroids(
        self,
        keys: t.Optional[t.Set[str]] = None, structured: bool = False,
    ) -> t.Dict[str, Array[1, 2]]:
        return {
            key: self.centroid(key, structured)
            for key in (keys or self._foam.fields)
        }

    def centroid_with_args(self, *keys: str, structured: bool = False) -> t.Dict[str, Array[1, 2]]:
        return self.centroids(set(keys), structured=structured)

    def probe(
        self,
        location: t.Tuple[float, float, float], keys: t.Optional[t.Set[str]] = None,
        point: bool = True, func: t.Optional[t.Callable] = None,
    ) -> t.Dict[str, Array[0, 1]]:
        location = tuple(map(float, location))
        return self.probes(location, keys=keys, point=point, func=func)[location]

    def probes(
        self,
        *locations: t.Tuple[float, float, float],
        keys: t.Optional[t.Set[str]] = None, point: bool = True, func: t.Optional[t.Callable] = None,
    ) -> t.Dict[t.Tuple[float, float, float], t.Dict[str, Array[0, 1]]]:
        '''
        - Reference:
            - https://github.com/OpenFOAM/OpenFOAM-7/tree/master/src/sampling/probes
        '''
        assert self._foam is not None

        keys = keys or self._foam.fields
        coords = self.points if point else self.cells
        fields = self.point_fields if point else self.cell_fields
        func = func or (lambda x: lib['numpy'].square(x).mean(axis=1))
        ans = {}
        for location in locations:
            index = lib['numpy'].argmin(func(coords-location))
            ans[tuple(map(float, location))] = {
                key: fields[key][index]
                for key in keys
            }
        return ans

    def _to_numpy(self, array: 'vtk.vtkCommonCore.vtkDataArray') -> Array[1, 2]:
        return lib['vtk_to_numpy'](array)
