__all__ = [
    'Ta', 'Tb', 'Tc',
    #
    'DictAny', 'DictFloat', 'DictStr', 'TupleSeq', 'Keys', 'Location',
    #
    'Any', 'DictAny2', 'DictStr2', 'DictStrAny', 'DictStrFloat', 'Document', 'FoamItem', 'FoamItems',
    'ListAny', 'ListFloat', 'ListInt', 'ListStr', 'Path',
    #
    'Array',
]


import pathlib as p
import typing as t

if t.TYPE_CHECKING:
    import numpy as _numpy


T1, T2, T3 = t.TypeVar('T1'), t.TypeVar('T2'), t.TypeVar('T3')
Ta, Tb, Tc = t.TypeVar('Ta'), t.TypeVar('Tb'), t.TypeVar('Tc')

DictAny = t.Dict[t.Hashable, T1]
DictFloat = t.Dict[float, T1]
DictStr = t.Dict[str, T1]
TupleSeq = t.Tuple[T1, ...]  # https://github.com/python/mypy/issues/184
Keys = t.Union[T1, TupleSeq[T1]]  # https://stackoverflow.com/questions/47190218/proper-type-hint-for-getitem
Location = t.Tuple[T1, T1, T1]

Any = t.Any
DictAny2 = DictAny[Any]
DictStr2 = DictStr[str]
DictStrAny = DictStr[Any]
DictStrFloat = DictStr[float]
ListAny = t.List[Any]
ListFloat = t.List[float]
ListInt = t.List[int]
ListStr = t.List[str]
Path = t.Union[str, p.Path]

Document = FoamItem = t.Union[DictStrAny, ListAny]
FoamItems = t.List[FoamItem]


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
