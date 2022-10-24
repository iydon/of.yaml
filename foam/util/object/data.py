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
    '''Multi-key dictionary

    Example:
        >>> data = Data.from_dict_keys(
        ...     ('left', 'x'), ('left', 'y'),
        ...     ('right', 'x'), ('right', 'y'),
        ...     default=list,
        ... )
        >>> data['left', 'x'].append({...})
        >>> data['right', 'y'].append({...})

        >>> for key, val in data.items():
        ...     print(key, val)
        ('left', 'x') [{Ellipsis}]
        ('left', 'y') []
        ('right', 'x') []
        ('right', 'y') [{Ellipsis}]
    '''

    def __init__(self, data: FoamItem) -> None:
        self._data = data

    def __contains__(self, keys: Keys[t.Any]) -> bool:
        if isinstance(keys, tuple):
            ans = self._data
            for key in keys:
                if key not in ans:
                    return False
                else:
                    ans = ans[key]
            return True
        elif isinstance(keys, list):
            return self.__contains__(tuple(keys))
        else:
            return self._data.__contains__(keys)

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
    def from_dict(cls, data: t.Optional[Dict] = None) -> 'Self':
        return cls({} if data is None else data)

    @classmethod
    def from_dict_keys(cls, *keys: t.Hashable, default: t.Callable = dict) -> 'Self':
        self = cls.from_dict()
        for key in keys:
            self[key] = default()
        return self

    @classmethod
    def from_list(cls, data: t.Optional[List] = None) -> 'Self':
        return cls([] if data is None else data)

    @classmethod
    def from_list_length(cls, length: int, default: t.Callable = lambda: None) -> 'Self':
        return cls.from_list([default() for _ in range(length)])

    @classmethod
    def load(cls, *paths: Path) -> t.Iterator['Self']:
        for path in map(p.Path, paths):
            yield cls.loads(path.read_bytes(), path.suffix[1:])

    @classmethod
    def load_from_path(cls, *parts: str) -> 'Self':
        return next(cls.load(p.Path(*parts)))

    @classmethod
    def loads(cls, content: bytes, type: str = 'yaml') -> 'Self':
        if type in {'json'}:
            data = json.loads(content)
        elif type in {'pickle', 'pkl'}:
            data = pickle.loads(content)
        elif type in {'yaml', 'yml'}:
            data = yaml.load_all(content)
        else:
            raise Exception(f'"{type}" is not a valid type string')
        return cls.from_any(data)

    @property
    def data(self) -> FoamItem:
        return self._data

    def contains(self, *keys: t.Any) -> bool:
        try:
            return self.__contains__(keys)
        except Exception:
            return False

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

    def dump_to_path(self, *parts: str) -> 'Self':
        return self.dump(p.Path(*parts))

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

    def set_default(self, *keys: t.Any, default: t.Any = None) -> 'Self':
        if keys not in self:
            self[keys] = default
        return self[keys]

    def set_via_dict(self, data: Dict) -> 'Self':
        for keys, value in self.__class__.from_dict(data).items():
            self[keys] = value
        return self

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

