__all__ = [
    'Ta', 'Tb', 'Tc',
    #
    'DictAny', 'DictFloat', 'DictStr', 'Func0', 'Func1', 'Func2', 'FuncAny', 'Generator',
    'TupleSeq', 'Keys', 'Triple',
    #
    'Any', 'DictAny2', 'DictStr2', 'DictStrAny', 'DictStrFloat', 'FuncAny2', 'ListAny',
    'ListFloat', 'ListInt', 'ListStr', 'SetPath', 'SetStr',
    #
    'Array0', 'Array1', 'Array2', 'Array01', 'Array12', 'Number',
    #
    'CmdItem', 'CmdItems', 'Document', 'FoamItem', 'FoamItems', 'Location', 'Path',
    #
    'ModuleType', 'NoneType',
]


import pathlib as p
import typing as t

if t.TYPE_CHECKING:
    import nptyping as npt


# type variables (private, public)
T1, T2, T3 = t.TypeVar('T1'), t.TypeVar('T2'), t.TypeVar('T3')
Ta, Tb, Tc = t.TypeVar('Ta'), t.TypeVar('Tb'), t.TypeVar('Tc')

# generics
DictAny = t.Dict[t.Hashable, T1]
DictFloat = t.Dict[float, T1]
DictStr = t.Dict[str, T1]
Func0 = t.Callable[[], T1]
Func1 = t.Callable[[T1], T2]
Func2 = t.Callable[[T1, T2], T3]
FuncAny = t.Callable[..., T1]
Generator = t.Generator[T1, None, None]  # TODO: Use Generator instead if Iterator
TupleSeq = t.Tuple[T1, ...]  # https://github.com/python/mypy/issues/184
Keys = t.Union[T1, TupleSeq[T1]]  # https://stackoverflow.com/questions/47190218/proper-type-hint-for-getitem
Triple = t.Tuple[T1, T1, T1]

# types with abstract names
Any = t.Any
DictAny2 = DictAny[Any]
DictStr2 = DictStr[str]
DictStrAny = DictStr[Any]
DictStrFloat = DictStr[float]
FuncAny2 = FuncAny[Any]
ListAny = t.List[Any]
ListFloat = t.List[float]
ListInt = t.List[int]
ListStr = t.List[str]
SetPath = t.Set[p.Path]
SetStr = t.Set[str]

Array0 = Number = t.Type['npt.Number']
Array1 = t.Type['npt.NDArray[npt.Shape["*"], npt.Floating]']
Array2 = t.Type['npt.NDArray[npt.Shape["*, *"], npt.Floating]']
Array01 = t.Union[Array0, Array1]
Array12 = t.Union[Array1, Array2]

# types with specific names (if several files use this type, put it here)
CmdItem = t.Union[str, DictStrAny]
CmdItems = t.List[CmdItem]
Document = FoamItem = t.Union[DictStrAny, ListAny]
FoamItems = t.List[FoamItem]
Location = Triple[float]
Path = t.Union[str, p.Path]

# others
ModuleType = type(t)
NoneType = type(None)
