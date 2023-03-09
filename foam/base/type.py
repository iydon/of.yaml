__all__ = ['Array', 'Dict', 'Document', 'FoamData', 'FoamItem', 'Keys', 'List', 'Location', 'Path', 'TupleSequence']


import pathlib as p
import typing as t

if t.TYPE_CHECKING:
    import typing_extensions as te

    import numpy as _numpy


T = t.TypeVar('T')

Dict = t.Dict[str, t.Any]
List = t.List[t.Any]
Document = FoamItem = t.Union[Dict, List]
FoamData = t.List[FoamItem]
Path = t.Union[str, p.Path]
TupleSequence = t.Tuple[T, ...]  # https://github.com/python/mypy/issues/184
Keys = t.Union[T, TupleSequence[T]]  # https://stackoverflow.com/questions/47190218/proper-type-hint-for-getitem


class Array:
    '''
    TODO:
        - https://github.com/ramonhagenaars/nptyping?
    '''

    def __class_getitem__(cls, dimensions: 'Keys[int]') -> t.Union['_numpy.number', '_numpy.ndarray']:
        if not isinstance(dimensions, tuple):
            return cls.__class_getitem__((dimensions, ))
        assert all(isinstance(d, int) and d>=0 for d in dimensions)

        if dimensions == (0, ):
            return '_numpy.number'
        else:
            return '_numpy.ndarray'


class Location:
    '''Location 3D'''

    def __class_getitem__(cls, T: type) -> type:
        return t.Tuple[T, T, T]

    @classmethod
    def cast(cls, location: 'te.Self', T: type) -> 'te.Self':
        return tuple(map(T, location))
