__all__ = ['Array', 'CachedLib', 'Dict', 'Keys', 'List', 'Location', 'Path']


import pathlib as p
import types
import typing as t


CachedLib = t.Union[types.ModuleType, object, t.Callable]
Dict = t.Dict[str, t.Any]
List = t.List[Dict]
Location = t.Tuple[float, float, float]
Path = t.Union[str, p.Path]


class Array:
    def __class_getitem__(cls, dimensions: 'Keys[int]') -> type:
        from .lib import lib

        if not isinstance(dimensions, tuple):
            dimensions = (dimensions, )
        assert all(isinstance(d, int) and d>=0 for d in dimensions)

        if t.TYPE_CHECKING:
            dimensions_ = set(dimensions)
            if dimensions_ == {0}:
                return lib['numpy'].number
            else:
                return lib['numpy'].ndarray
        else:
            return t.Any


class Keys:
    def __class_getitem__(cls, T: type) -> type:
        return t.Union[T, t.Tuple[T, ...]]
