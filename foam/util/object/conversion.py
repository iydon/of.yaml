__all__ = ['Conversion']


import json
import pathlib as p
import pickle
import typing as t

from ...base.lib import tomlkit, yaml
from ...base.type import Document, Path

if t.TYPE_CHECKING:
    from typing_extensions import Self


class Conversion:
    '''Conversion between object and bytes/string

    Example:
        >>> data = {'a': 1, 'b': [2, 3], 'c': {'4': 5}}
        >>> print(Conversion.from_document(data).to_yaml())
        a: 1
        b:
        - 2
        - 3
        c:
        '4': 5
    '''

    _alias = {'pkl': 'pickle', 'yml': 'yaml'}
    _types = {'json', 'pickle', 'toml', 'yaml'}

    def __init__(self, document: Document) -> None:
        self._document = document

    @classmethod
    def auto_from_bytes(cls, content: bytes, all: bool = False) -> 'Self':
        for type in cls._types:
            try:
                return cls.from_bytes(content, type, all)
            except Exception:
                pass
        raise Exception('Unable to recognize content type')

    @classmethod
    def auto_from_string(cls, text: str, all: bool = False) -> 'Self':
        return cls.auto_from_bytes(text.encode(), all)

    @classmethod
    def auto_from_path(cls, path: Path, all: bool = False) -> 'Self':
        return cls.auto_from_bytes(p.Path(path).read_bytes(), all)

    @classmethod
    def from_document(cls, document: Document) -> 'Self':
        return cls(document)

    @classmethod
    def from_bytes(cls, content: bytes, type_or_suffix: str = 'json', all: bool = False) -> 'Self':
        type = cls.type_from_suffix(type_or_suffix)
        if type not in cls._types:
            raise Exception(f'"{type}" is not a valid type string')
        else:
            return {
                'json': lambda content: cls.from_json(content.decode()),
                'pickle': lambda content: cls.from_pickle(content),
                'toml': lambda content: cls.from_toml(content.decode()),
                'yaml': lambda content: cls.from_yaml(content.decode(), all),
            }[type](content)

    @classmethod
    def from_string(cls, text: str, type: str = 'json', all: bool = False) -> 'Self':
        return cls.from_bytes(text.encode(), type, all)

    @classmethod
    def from_path(cls, path: Path, all: bool = False, type: t.Optional[str] = None) -> 'Self':
        path = p.Path(path)
        type_or_suffix = path.suffix if type is None else type  # type or path.suffix
        return cls.from_bytes(path.read_bytes(), type_or_suffix, all)

    @classmethod
    def from_json(cls, text: str) -> 'Self':
        return cls(json.loads(text))

    @classmethod
    def from_pickle(cls, text: bytes) -> 'Self':
        return cls(pickle.loads(text))

    @classmethod
    def from_toml(cls, text: str) -> 'Self':
        return cls(tomlkit.loads(text))

    @classmethod
    def from_yaml(cls, text: str, all: bool = False) -> 'Self':
        document = list(yaml.load_all(text)) if all else yaml.load(text)
        return cls(document)

    @classmethod
    def type_from_suffix(self, type_or_suffix: str) -> str:
        type = type_or_suffix.lstrip('.')
        return self._alias.get(type, type)  # assert _ in self._types

    @classmethod
    def suffixes(cls, dot: bool = True) -> t.Set[str]:
        ans = cls._types | cls._alias.keys()
        if dot:
            ans = set(map(lambda x: f'.{x}', ans))
        return ans

    def to_document(self) -> Document:
        return self._document

    def to_bytes(self, type_or_suffix: str = 'json', all: bool = False, **kwargs: t.Any) -> bytes:
        type = self.type_from_suffix(type_or_suffix)
        if type not in self._types:
            raise Exception(f'"{type}" is not a valid type string')
        else:
            return {
                'json': lambda: self.to_json(**kwargs).encode(),
                'pickle': lambda: self.to_pickle(**kwargs),
                'toml': lambda: self.to_toml(**kwargs).encode(),
                'yaml': lambda: self.to_yaml(all, **kwargs).encode(),
            }[type]()

    def to_string(self, type: str = 'json', all: bool = False, **kwargs: t.Any) -> str:
        return self.to_bytes(type, all, **kwargs).decode()

    def to_path(self, path: Path, all: bool = False, type: t.Optional[str] = None, **kwargs: t.Any) -> p.Path:
        path = p.Path(path)
        type_or_suffix = path.suffix if type is None else type  # type or path.suffix
        path.write_bytes(self.to_bytes(type_or_suffix, all, **kwargs))
        return path

    def to_json(self, **kwargs: t.Any) -> str:
        kwargs = {'ensure_ascii': False, **kwargs}
        return json.dumps(self._document, **kwargs)

    def to_pickle(self, **kwargs: t.Any) -> bytes:
        return pickle.dumps(self._document, **kwargs)

    def to_toml(self, **kwargs: t.Any) -> str:
        return tomlkit.dumps(self._document, **kwargs)

    def to_yaml(self, all: bool = False, **kwargs: t.Any) -> str:
        kwargs = {'indent': 4, **kwargs}
        return (yaml.dump_all if all else yaml.dump)(self._document, **kwargs)
