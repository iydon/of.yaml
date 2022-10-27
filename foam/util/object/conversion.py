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

    types = {'json', 'pickle', 'toml', 'yaml'}

    def __init__(self, document: Document) -> None:
        self._document = document

    @classmethod
    def auto_from_bytes(cls, content: bytes, all: bool = False) -> 'Self':
        for type in cls.types:
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
    def from_bytes(cls, content: bytes, type: str = 'json', all: bool = False) -> 'Self':
        type = type.lstrip('.')
        for types, loads in [
            ({'json'}, lambda content: cls.from_json(content.decode())),
            ({'pickle', 'pkl'}, lambda content: cls.from_pickle(content)),
            ({'toml'}, lambda content: cls.from_toml(content.decode())),
            ({'yaml', 'yml'}, lambda content: cls.from_yaml(content.decode(), all)),
        ]:
            if type in types:
                return loads(content)
        raise Exception(f'"{type}" is not a valid type string')

    @classmethod
    def from_string(cls, text: str, type: str = 'json', all: bool = False) -> 'Self':
        return cls.from_bytes(text.encode(), type, all)

    @classmethod
    def from_path(cls, path: Path, all: bool = False) -> 'Self':
        path = p.Path(path)
        return cls.from_bytes(path.read_bytes(), path.suffix[1:], all)

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

    def to_document(self) -> Document:
        return self._document

    def to_bytes(self, type: str = 'json', all: bool = False, **kwargs: t.Any) -> bytes:
        type = type.lstrip('.')
        for types, dumps in [
            ({'json'}, lambda: self.to_json(**kwargs).encode()),
            ({'pickle', 'pkl'}, lambda: self.to_pickle(**kwargs)),
            ({'toml'}, lambda: self.to_toml(**kwargs).encode()),
            ({'yaml', 'yml'}, lambda: self.to_yaml(all, **kwargs).encode()),
        ]:
            if type in types:
                return dumps()
        raise Exception(f'"{type}" is not a valid type string')

    def to_string(self, type: str = 'json', all: bool = False, **kwargs: t.Any) -> str:
        return self.to_bytes(type, all, **kwargs).decode()

    def to_path(self, path: Path, all: bool = False, **kwargs: t.Any) -> p.Path:
        path = p.Path(path)
        path.write_bytes(self.to_bytes(path.suffix[1:], all, **kwargs))
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
