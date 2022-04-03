__all__ = ['Dict', 'List', 'Path', 'Data']


import pathlib as p
import typing as t


Dict = t.Dict[str, t.Any]
List = t.List[Dict]
Path = t.Union[str, p.Path]


class Data:
    def __init__(self, data: t.Union[Dict, List]) -> None:
        self._data = data

    def __getitem__(self, keys: t.Any) -> t.Any:
        if isinstance(keys, tuple):
            ans = self._data
            for key in keys:
                ans = ans[key]
            return ans
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
        return self._data.get(key, default)
