__all__ = ['Array', 'CachedLib', 'Dict', 'FoamData', 'FoamItem', 'Keys', 'List', 'Location', 'Path', 'TupleSequence']


import pathlib as p
import types
import typing as t

if t.TYPE_CHECKING:
    import numpy as _numpy


CachedLib = t.Union[types.ModuleType, object, t.Callable]
Dict = t.Dict[str, t.Any]
List = t.List[t.Any]
FoamItem = t.Union[Dict, List]
FoamData = t.List[FoamItem]
Location = t.Tuple[float, float, float]
Path = t.Union[str, p.Path]


class Array:
    # TODO: https://github.com/ramonhagenaars/nptyping?

    def __class_getitem__(cls, dimensions: 'Keys[int]') -> t.Union['_numpy.number', '_numpy.ndarray']:
        if not isinstance(dimensions, tuple):
            return cls.__class_getitem__((dimensions, ))
        assert all(isinstance(d, int) and d>=0 for d in dimensions)

        if dimensions == (0, ):
            return '_numpy.number'
        else:
            return '_numpy.ndarray'


class Keys:
    # TODO: https://stackoverflow.com/questions/47190218/proper-type-hint-for-getitem

    def __class_getitem__(cls, T: type) -> type:
        return t.Union[T, TupleSequence[T]]


class TupleSequence:
    # Reference: https://github.com/python/mypy/issues/184

    def __class_getitem__(cls, T: type) -> type:
        return t.Tuple[T, ...]
