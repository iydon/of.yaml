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

    def __init__(self, document: Document) -> None:
        self._document = document

    @classmethod
    def auto_from_bytes(cls, content: bytes) -> 'Self':
        for type in {'json', 'pickle', 'toml', 'yaml'}:
            try:
                return cls.from_bytes(content, type)
            except Exception:
                pass
        raise Exception('Unable to recognize content type')

    @classmethod
    def auto_from_string(cls, text: str) -> 'Self':
        # TODO: return cls.auto_from_bytes(text.encode())
        for type in {'json', 'toml', 'yaml'}:
            try:
                return cls.from_string(text, type)
            except Exception:
                pass
        raise Exception('Unable to recognize text type')

    @classmethod
    def auto_from_path(cls, path: Path) -> 'Self':
        return cls.auto_from_bytes(p.Path(path).read_bytes())

    @classmethod
    def from_document(cls, document: Document) -> 'Self':
        return cls(document)

    @classmethod
    def from_bytes(cls, content: bytes, type: str = 'json') -> 'Self':
        type = type.lstrip('.')
        for types, loads in [
            ({'json'}, lambda content: cls.from_json(content.decode())),
            ({'pickle', 'pkl'}, lambda content: cls.from_pickle(content)),
            ({'toml'}, lambda content: cls.from_toml(content.decode())),
            ({'yaml', 'yml'}, lambda content: cls.from_yaml(content.decode())),
        ]:
            if type in types:
                return loads(content)
        raise Exception(f'"{type}" is not a valid type string')

    @classmethod
    def from_string(cls, text: str, type: str = 'json') -> 'Self':
        # TODO: return cls.from_bytes(text.encode(), type)
        type = type.lstrip('.')
        for types, loads in [
            ({'json'}, cls.from_json),
            ({'toml'}, cls.from_toml),
            ({'yaml', 'yml'}, cls.from_yaml),
        ]:
            if type in types:
                return loads(text)
        raise Exception(f'"{type}" is not a valid type string')

    @classmethod
    def from_path(cls, path: Path) -> 'Self':
        path = p.Path(path)
        return cls.from_bytes(path.read_bytes(), path.suffix[1:])

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
    def from_yaml(cls, text: str) -> 'Self':
        return cls(yaml.load(text))

    @classmethod
    def from_yaml_all(cls, text: str) -> 'Self':
        return cls(list(yaml.load_all(text)))

    def to_document(self) -> Document:
        return self._document

    def to_bytes(self, type: str = 'json') -> bytes:
        type = type.lstrip('.')
        for types, dumps in [
            ({'json'}, lambda: self.to_json().encode()),
            ({'pickle', 'pkl'}, lambda: self.to_pickle()),
            ({'toml'}, lambda: self.to_toml().encode()),
            ({'yaml', 'yml'}, lambda: self.to_yaml().encode()),
        ]:
            if type in types:
                return dumps()
        raise Exception(f'"{type}" is not a valid type string')

    def to_string(self, type: str = 'json') -> str:
        type = type.lstrip('.')
        for types, dumps in [
            ({'json'}, self.to_json),
            ({'toml'}, self.to_toml),
            ({'yaml', 'yml'}, self.to_yaml),
        ]:
            if type in types:
                return dumps()
        raise Exception(f'"{type}" is not a valid type string')

    def to_path(self, path: Path) -> p.Path:
        path = p.Path(path)
        path.write_bytes(self.to_bytes(path.suffix[1:]))
        return path

    def to_json(self) -> str:
        return json.dumps(self._document)

    def to_pickle(self) -> bytes:
        return pickle.dumps(self._document)

    def to_toml(self) -> str:
        return tomlkit.dumps(self._document)

    def to_yaml(self) -> str:
        return yaml.dump(self._document)

    def to_yaml_all(self) -> str:
        return yaml.dump_all(self._document)
