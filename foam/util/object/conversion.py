__all__ = ['Conversion']


import json
import pathlib as p
import pickle
import typing as t

from ..function import deprecated_classmethod
from ...base.lib import tomlkit, yaml
from ...base.type import Document, Path, SetStr

if t.TYPE_CHECKING:
    import typing_extensions as te

    P = te.ParamSpec('P')
    Kwargs = te.ParamSpecKwargs(P)


class Conversion:
    '''Conversion between object and bytes/string

    Example:
        >>> data = {'a': 1, 'b': [2, 3], 'c': {'4': 5}}
        >>> print(Conversion.fromDocument(data).to_yaml())
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
    def autoFromBytes(cls, content: bytes, all: bool = False) -> 'te.Self':
        for type in cls._types:
            try:
                return cls.fromBytes(content, type, all)
            except Exception:
                pass
        raise Exception('Unable to recognize content type')

    @classmethod
    def autoFromString(cls, text: str, all: bool = False) -> 'te.Self':
        return cls.autoFromBytes(text.encode(), all)

    @classmethod
    def autoFromPath(cls, path: Path, all: bool = False) -> 'te.Self':
        return cls.autoFromBytes(p.Path(path).read_bytes(), all)

    @classmethod
    def fromDocument(cls, document: Document) -> 'te.Self':
        return cls(document)

    @classmethod
    def fromBytes(cls, content: bytes, type_or_suffix: str = 'json', all: bool = False) -> 'te.Self':
        type = cls.typeFromSuffix(type_or_suffix)
        if type not in cls._types:
            raise Exception(f'"{type}" is not a valid type string')
        else:
            return {
                'json': lambda content: cls.fromJSON(content.decode()),
                'pickle': lambda content: cls.fromPickle(content),
                'toml': lambda content: cls.fromTOML(content.decode()),
                'yaml': lambda content: cls.fromYAML(content.decode(), all),
            }[type](content)

    @classmethod
    def fromString(cls, text: str, type: str = 'json', all: bool = False) -> 'te.Self':
        return cls.fromBytes(text.encode(), type, all)

    @classmethod
    def fromPath(cls, path: Path, all: bool = False, type: t.Optional[str] = None) -> 'te.Self':
        path = p.Path(path)
        type_or_suffix = path.suffix if type is None else type  # type or path.suffix
        return cls.fromBytes(path.read_bytes(), type_or_suffix, all)

    @classmethod
    def fromJSON(cls, text: str) -> 'te.Self':
        return cls(json.loads(text))

    @classmethod
    def fromPickle(cls, text: bytes) -> 'te.Self':
        return cls(pickle.loads(text))

    @classmethod
    def fromTOML(cls, text: str) -> 'te.Self':
        return cls(tomlkit.loads(text))

    @classmethod
    def fromYAML(cls, text: str, all: bool = False) -> 'te.Self':
        document = list(yaml.load_all(text)) if all else yaml.load(text)
        return cls(document)

    @classmethod
    def typeFromSuffix(self, type_or_suffix: str) -> str:
        type = type_or_suffix.lstrip('.')
        return self._alias.get(type, type)  # assert _ in self._types

    @classmethod
    def suffixes(cls, dot: bool = True) -> SetStr:
        ans = cls._types | cls._alias.keys()
        if dot:
            ans = set(map(lambda x: f'.{x}', ans))
        return ans

    def to_document(self) -> Document:
        return self._document

    def to_bytes(self, type_or_suffix: str = 'json', all: bool = False, **kwargs: 'Kwargs') -> bytes:
        type = self.typeFromSuffix(type_or_suffix)
        if type not in self._types:
            raise Exception(f'"{type}" is not a valid type string')
        else:
            return {
                'json': lambda: self.to_json(**kwargs).encode(),
                'pickle': lambda: self.to_pickle(**kwargs),
                'toml': lambda: self.to_toml(**kwargs).encode(),
                'yaml': lambda: self.to_yaml(all, **kwargs).encode(),
            }[type]()

    def to_string(self, type: str = 'json', all: bool = False, **kwargs: 'Kwargs') -> str:
        return self.to_bytes(type, all, **kwargs).decode()

    def to_path(self, path: Path, all: bool = False, type: t.Optional[str] = None, **kwargs: 'Kwargs') -> p.Path:
        path = p.Path(path)
        type_or_suffix = path.suffix if type is None else type  # type or path.suffix
        path.write_bytes(self.to_bytes(type_or_suffix, all, **kwargs))
        return path

    def to_json(self, **kwargs: 'Kwargs') -> str:
        kwargs = {'ensure_ascii': False, **kwargs}
        return json.dumps(self._document, **kwargs)

    def to_pickle(self, **kwargs: 'Kwargs') -> bytes:
        return pickle.dumps(self._document, **kwargs)

    def to_toml(self, **kwargs: 'Kwargs') -> str:
        return tomlkit.dumps(self._document, **kwargs)

    def to_yaml(self, all: bool = False, **kwargs: 'Kwargs') -> str:
        kwargs = {'indent': 4, **kwargs}
        return (yaml.dump_all if all else yaml.dump)(self._document, **kwargs)

    auto_from_bytes = deprecated_classmethod(autoFromBytes)
    auto_from_string = deprecated_classmethod(autoFromString)
    auto_from_path = deprecated_classmethod(autoFromPath)
    from_document = deprecated_classmethod(fromDocument)
    from_bytes = deprecated_classmethod(fromBytes)
    from_string = deprecated_classmethod(fromString)
    from_path = deprecated_classmethod(fromPath)
    from_json = deprecated_classmethod(fromJSON, 'from_json')
    from_pickle = deprecated_classmethod(fromPickle)
    from_toml = deprecated_classmethod(fromTOML, 'from_toml')
    from_yaml = deprecated_classmethod(fromYAML, 'from_yaml')
    type_from_suffix = deprecated_classmethod(typeFromSuffix)
