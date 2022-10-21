__all__ = ['Data']


import json
import pathlib as p
import pickle
import typing as t

from ...base.lib import yaml
from ...base.type import Dict, FoamItem, Keys, List, Path

if t.TYPE_CHECKING:
    from typing_extensions import Self


class Data:
    def __init__(self, data: FoamItem) -> None:
        self._data = data

    def __getitem__(self, keys: Keys[t.Any]) -> t.Any:
        if isinstance(keys, tuple):
            ans = self._data
            for key in keys:
                ans = ans[key]
            return ans
        elif isinstance(keys, list):
            # TODO: DeprecationWarning
            return self.__getitem__(tuple(keys))
        else:
            return self._data[keys]

    def __setitem__(self, keys: Keys[t.Any], value: t.Any) -> None:
        if isinstance(keys, tuple):
            assert keys

            ans = self._data
            for key in keys[:-1]:
                if isinstance(ans, dict):
                    ans = ans.setdefault(key, {})
                elif isinstance(ans, list):
                    ans = ans[key]
                else:
                    raise Exception(f'Unknown type "{type(ans).__name__}"')
            ans[keys[-1]] = value
        elif isinstance(keys, list):
            # TODO: DeprecationWarning
            self.__setitem__(tuple(keys), value)
        else:
            self._data[keys] = value

    def __bool__(self) -> bool:
        return bool(self._data)  # 'list' object has no attribute '__bool__'

    def __iter__(self) -> t.Iterator[t.Any]:
        return self._data.__iter__()

    def __len__(self) -> int:
        return self._data.__len__()

    def __repr__(self) -> str:
        return f'Data({self._data!r})'

    def __str__(self) -> str:
        return self._data.__str__()

    @classmethod
    def from_any(cls, data: FoamItem) -> 'Self':
        return cls(data)

    @classmethod
    def from_dict(cls, data: Dict = {}) -> 'Self':
        return cls(data)

    @classmethod
    def from_list(cls, data: List = []) -> 'Self':
        return cls(data)

    @property
    def data(self) -> FoamItem:
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

    def items(self, with_list: bool = False) -> t.Iterator[t.Tuple[Keys[t.Any], t.Any]]:
        yield from self._items(self._data, with_list=with_list)

    def dump(self, *paths: Path) -> 'Self':
        for path in map(p.Path, paths):
            path.write_bytes(self.dumps(path.suffix[1:]))
        return self

    def dumps(self, type: str = 'yaml', **kwargs: t.Any) -> bytes:
        if type in {'json'}:
            kwargs = {'ensure_ascii': False, **kwargs}
            return json.dumps(self._data, **kwargs).encode()
        elif type in {'pickle', 'pkl'}:
            return pickle.dumps(self._data, **kwargs)
        elif type in {'yaml', 'yml'}:
            kwargs = {'indent': 4, **kwargs}
            return yaml.dump_all(self._data, **kwargs).encode()
        else:
            raise Exception(f'"{type}" is not a valid type string')

    def _items(
        self,
        data: t.Any, with_list: bool = False, keys: Keys[t.Any] = (),
    ) -> t.Iterator[t.Tuple[Keys[t.Any], t.Any]]:
        if isinstance(data, dict):
            for key, value in data.items():
                yield from self._items(value, with_list, keys+(key, ))
        elif with_list and isinstance(data, list):
            for key, value in enumerate(data):
                yield from self._items(value, with_list, keys+(key, ))
        else:
            yield keys, data

