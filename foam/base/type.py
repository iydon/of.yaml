__all__ = ['Array', 'CachedLib', 'Dict', 'Keys', 'List', 'Path', 'Data', 'Version']


import pathlib as p
import types
import typing as t


CachedLib = t.Union[types.ModuleType, object, t.Callable]
Dict = t.Dict[str, t.Any]
Keys = t.Tuple[t.Any, ...]
List = t.List[Dict]
Path = t.Union[str, p.Path]


class Array:
    def __class_getitem__(cls, dimensions: t.Union[int, t.Tuple[int, ...]]) -> type:
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


class Data:
    def __init__(self, data: t.Union[Dict, List]) -> None:
        self._data = data

    def __getitem__(self, keys: t.Any) -> t.Any:
        if isinstance(keys, tuple):
            ans = self._data
            for key in keys:
                ans = ans[key]
            return ans
        elif isinstance(keys, list):
            return self.__getitem__(tuple(keys))
        else:
            return self._data[keys]

    def __setitem__(self, keys: t.Any, value: t.Any) -> None:
        if isinstance(keys, tuple):
            assert keys

            ans = self._data
            for key in keys[:-1]:
                if isinstance(ans, dict):
                    ans = ans.setdefault(key, {})
                elif isinstance(ans, list):
                    ans = ans[key]
                else:
                    raise Exception
            ans[keys[-1]] = value
        elif isinstance(keys, list):
            self.__setitem__(tuple(keys), value)
        else:
            self._data[keys] = value

    def __bool__(self) -> bool:
        return bool(self._data)  # 'list' object has no attribute '__bool__'

    def __iter__(self) -> t.Iterator[t.Any]:
        return self._data.__iter__()

    def __repr__(self) -> str:
        return self._data.__repr__()

    @property
    def data(self) -> t.Union[Dict, List]:
        return self._data

    def get(self, key: t.Any, default: t.Optional[t.Any] = None) -> t.Any:
        if isinstance(self._data, dict):
            return self._data.get(key, default)
        elif isinstance(self._data, list):
            try:
                return self._data[key]
            except (IndexError, TypeError):
                return default
        else:
            raise

    def items(self, with_list: bool = False) -> t.Iterator[t.Tuple[Keys, t.Any]]:
        yield from self._items(self._data, with_list=with_list)

    def _items(self, data: t.Any, with_list: bool = False, keys: Keys = ()) -> t.Iterator[t.Tuple[Keys, t.Any]]:
        if isinstance(data, dict):
            for key, value in data.items():
                yield from self._items(value, with_list, keys+(key, ))
        elif with_list and isinstance(data, list):
            for key, value in enumerate(data):
                yield from self._items(value, with_list, keys+(key, ))
        else:
            yield keys, data


class Version(t.NamedTuple):
    major: int
    minor: int
    micro: int = 0
