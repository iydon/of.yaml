__all__ = ['Data']


import pathlib as p
import typing as t

from .conversion import Conversion
from ..function import deprecated_classmethod
from ...base.type import Any, DictStrAny, FoamItem, Keys, ListAny, Path

if t.TYPE_CHECKING:
    import typing_extensions as te

    P = te.ParamSpec('P')
    Args = te.ParamSpecArgs(P)
    Kwargs = te.ParamSpecKwargs(P)


class Data:
    '''Multi-key dictionary or list (not recommended)

    Example:
        >>> data = Data.fromDictKeys(
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

    def __contains__(self, keys: Keys[Any]) -> bool:
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

    def __getitem__(self, keys: Keys[Any]) -> Any:
        if isinstance(keys, tuple):
            ans = self._data
            for key in keys:
                ans = ans[key]
            return ans
        elif isinstance(keys, list):
            # TODO: throw DeprecationWarning
            return self.__getitem__(tuple(keys))
        else:
            return self._data[keys]

    def __setitem__(self, keys: Keys[Any], value: Any) -> None:
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
            # TODO: throw DeprecationWarning
            self.__setitem__(tuple(keys), value)
        else:
            self._data[keys] = value

    def __bool__(self) -> bool:
        return bool(self._data)  # 'list' object has no attribute '__bool__'

    def __iter__(self) -> t.Iterator[Any]:
        return self._data.__iter__()

    def __len__(self) -> int:
        return self._data.__len__()

    def __repr__(self) -> str:
        return f'Data({self._data!r})'

    def __str__(self) -> str:
        return self._data.__str__()

    @classmethod
    def fromAny(cls, data: FoamItem) -> 'te.Self':
        return cls(data)

    @classmethod
    def fromDict(cls, data: t.Optional[DictStrAny] = None) -> 'te.Self':
        return cls({} if data is None else data)

    @classmethod
    def fromDictKeys(cls, *keys: t.Hashable, default: t.Optional[t.Callable] = None) -> 'te.Self':
        func = default or dict
        self = cls.fromDict()
        for key in keys:
            self.__setitem__(key, func())
        return self

    @classmethod
    def fromList(cls, data: t.Optional[ListAny] = None) -> 'te.Self':
        return cls([] if data is None else data)

    @classmethod
    def fromListLength(cls, length: int, default: t.Optional[t.Callable] = None) -> 'te.Self':
        func = default or (lambda: None)
        return cls.fromList([func() for _ in range(length)])

    @classmethod
    def load(cls, *paths: Path, type: t.Optional[str] = None) -> t.Iterator['te.Self']:
        for path in map(p.Path, paths):
            type_or_suffix = path.suffix if type is None else type  # type or path.suffix
            yield cls.loads(path.read_bytes(), type_or_suffix)

    @classmethod
    def loadFromPath(cls, *parts: str, type: t.Optional[str] = None) -> 'te.Self':
        return next(cls.load(p.Path(*parts), type))

    @classmethod
    def loads(cls, content: bytes, type_or_suffix: str = 'yaml') -> 'te.Self':
        return cls.fromAny(Conversion.fromBytes(content, type_or_suffix, all=True).to_document())

    @property
    def data(self) -> FoamItem:
        return self._data

    def dump(self, *paths: Path, type: t.Optional[str] = None) -> 'te.Self':
        for path in map(p.Path, paths):
            type_or_suffix = path.suffix if type is None else type  # type or path.suffix
            path.write_bytes(self.dumps(type_or_suffix))
        return self

    def dump_to_path(self, *parts: str, type: t.Optional[str] = None) -> 'te.Self':
        return self.dump(p.Path(*parts), type)

    def dumps(self, type_or_suffix: str = 'yaml', **kwargs: 'Kwargs') -> bytes:
        return Conversion \
            .fromDocument(self._data) \
            .to_bytes(type_or_suffix, all=True, **kwargs)

    def is_dict(self) -> bool:
        return isinstance(self._data, dict)

    def is_list(self) -> bool:
        return isinstance(self._data, list)

    def is_other(self) -> bool:
        return not (self.is_dict() or self.is_list())

    def to_any(self) -> FoamItem:
        return self._data

    def to_dict(self) -> DictStrAny:
        assert self.is_dict()

        return self._data

    def to_list(self) -> ListAny:
        assert self.is_list()

        return self._data

    def contains(self, *keys: 'Args') -> bool:
        try:
            return self.__contains__(keys)
        except Exception:
            return False

    def get(self, key: Any, default: t.Optional[Any] = None) -> Any:
        # TODO: retained due to compatibility needs
        if isinstance(self._data, dict):
            return self._data.get(key, default)
        elif isinstance(self._data, list):
            try:
                return self._data[key]
            except (IndexError, TypeError):
                return default
        else:
            raise Exception(f'Unknown type "{type(self._data).__name__}"')

    def gets(self, *keys: 'Args', default: t.Optional[Any] = None) -> Any:
        try:
            return self.__getitem__(keys)
        except (IndexError, KeyError, TypeError):
            return default

    def setdefault(self, key: Any, default: t.Optional[Any] = None) -> Any:
        # TODO: retained due to compatibility needs
        return self._data.setdefault(key, default)

    def set_default(self, *keys: 'Args', default: t.Optional[Any] = None) -> 'te.Self':
        if keys not in self:
            self.__setitem__(keys, default)
        return self.__getitem__(keys)

    def set_via_dict(self, data: DictStrAny) -> 'te.Self':
        for keys, value in self.__class__.fromDict(data).items():
            self.__setitem__(keys, value)
        return self

    def items(self, with_list: bool = False) -> t.Iterator[t.Tuple[Keys[Any], Any]]:
        yield from self._items(self._data, with_list=with_list)

    def _items(
        self,
        data: Any, with_list: bool = False, keys: Keys[Any] = (),
    ) -> t.Iterator[t.Tuple[Keys[Any], Any]]:
        if isinstance(data, dict):
            for key, value in data.items():
                yield from self._items(value, with_list, keys+(key, ))
        elif with_list and isinstance(data, list):
            for key, value in enumerate(data):
                yield from self._items(value, with_list, keys+(key, ))
        else:
            yield keys, data

    from_any = deprecated_classmethod(fromAny)
    from_dict = deprecated_classmethod(fromDict)
    from_dict_keys = deprecated_classmethod(fromDictKeys)
    from_list = deprecated_classmethod(fromList)
    from_list_length = deprecated_classmethod(fromListLength)
    load_from_path = deprecated_classmethod(loadFromPath)
