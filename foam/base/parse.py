__all__ = ['Parser']


import functools as f
import io
import json
import pathlib as p
import shutil
import sys
import typing as t
import urllib.parse
import urllib.request

from .lib import lib
from .type import Dict
from ..util.object import Data

if t.TYPE_CHECKING:
    from typing_extensions import Self

    from .core import Foam


class register:
    '''Register'''

    static_methods = {}
    url_methods = {}

    @classmethod
    def static(cls, *types: str) -> t.Callable:
        '''Register processing methods for different types'''

        def decorate(func: t.Callable) -> t.Callable:
            cls.static_methods[types] = func

            @f.wraps(func)
            def wrapper(*args: t.Any, **kwargs: t.Any) -> t.Any:
                return func(*args, **kwargs)

            return wrapper

        return decorate

    @classmethod
    def url(cls, *types: str) -> t.Callable:
        '''See register::static method for details'''

        def decorate(func: t.Callable) -> t.Callable:
            cls.url_methods[types] = func

            @f.wraps(func)
            def wrapper(*args: t.Any, **kwargs: t.Any) -> t.Any:
                return func(*args, **kwargs)

            return wrapper

        return decorate


class Static:
    '''OpenFOAM static parser'''

    def __init__(self, foam: 'Foam') -> None:
        self._foam = foam

    def __getitem__(self, keys: t.Tuple[str, ...]) -> t.Callable:
        try:
            return lambda *args, **kwargs: register.static_methods[keys](self, *args, **kwargs)
        except KeyError:
            raise Exception(f'Unknown types "{keys}"')

    @classmethod
    def from_foam(cls, foam: 'Foam') -> 'Self':
        return cls(foam)

    @register.static()
    def _(self, static: Dict) -> None:
        # do nothing
        pass

    @register.static('embed', 'text')
    def _(self, static: Dict) -> None:
        out = self._out(static['name'])
        self._foam._write(out, static['data'], static.get('permission', None))

    @register.static('embed', 'binary')
    def _(self, static: Dict) -> None:
        out = self._out(static['name'])
        out.write_bytes(static['data'])

    @register.static('embed', '7z')
    def _(self, static: Dict) -> None:
        self._assert()
        out = self._out(static['name'])
        with lib['py7zr'].SevenZipFile(io.BytesIO(static['data']), mode='r') as z:
            z.extractall(path=out.parent)

    @register.static('path', 'raw')
    def _(self, static: Dict) -> None:
        out, in_ = self._out(static['name']), self._in(static['data'])
        if in_.is_dir():
            kwargs = {'dirs_exist_ok': True} if sys.version_info >= (3, 8) else {}
            shutil.copytree(in_, out, **kwargs)
        elif in_.is_file():
            shutil.copyfile(in_, out)
        else:
            raise Exception('Target is neither a file nor a directory')

    @register.static('path', '7z')
    def _(self, static: Dict) -> None:
        self._assert()
        out, in_ = self._out(static['name']), self._in(static['data'])
        with lib['py7zr'].SevenZipFile(in_, mode='r') as z:
            z.extractall(path=out.parent)

    @register.static('path', 'foam', 'json')
    def _(self, static: Dict) -> None:
        self._path_foam(static)

    @register.static('path', 'foam', 'yaml')
    def _(self, static: Dict) -> None:
        self._path_foam(static)

    def _out(self, name: str) -> p.Path:
        out = self._foam._path(name)  # self._foam._dest is not None
        out.parent.mkdir(parents=True, exist_ok=True)
        return out

    def _in(self, data: str) -> p.Path:
        return self._foam._root / data

    def _assert(self) -> None:
        assert lib['py7zr'] is not None, 'pip install ifoam[7z]'  # TODO: improve error message

    def _path_foam(self, static: Dict) -> None:
        data = Data.from_dict({})
        out, in_ = self._foam._path(), self._in(static['data'])
        data[static['name'].split('/')] = {  # p.Path(static['name']).parts
            'json': lambda path: json.loads(path.read_text()),
            'yaml': lambda path: lib['yaml'].load(path.read_text(), Loader=lib['SafeLoader']),
        }[static['type'][2]](in_)
        self._foam.__class__([{'order': ['meta', 'foam']}, data._data], in_.parent, warn=False) \
            .save(out, paraview=False)


class Url:
    '''Merge remote multiple files into a single file'''

    def __init__(self, foam: 'Foam') -> None:
        self._foam = foam
        self._path = None
        self._url = None

    def __getitem__(self, keys: t.Tuple[str, ...]) -> t.Callable:
        method = register.url_methods.get(keys, lambda self, static: static)
        return lambda *args, **kwargs: method(self, *args, **kwargs)

    @classmethod
    def from_foam(cls, foam: 'Foam') -> 'Self':
        return cls(foam)

    @property
    def path(self) -> p.Path:
        return self._path

    @property
    def root(self) -> p.Path:
        return self._path.parent

    @property
    def url(self) -> str:
        return urllib.parse.urlunsplit(self._url)

    def set_url(self, url: str) -> 'Self':
        self._url = urllib.parse.urlsplit(url)
        self._path = p.Path(self._url.path)
        return self

    def set_split_url(self, split_url: urllib.parse.SplitResult) -> 'Self':
        self._url = split_url
        self._path = p.Path(split_url.path)
        return self

    def url_from_path(self, path: p.Path) -> str:
        parts = list(self._url)
        parts[2] = path.as_posix()
        return urllib.parse.urlunsplit(parts)

    @register.url('path', 'raw')
    def _(self, static: Dict) -> Dict:
        # TODO: directory
        url = self.url_from_path(self.root/static['data'])
        static.update({'type': ['embed', 'binary'], 'data': self._urlopen(url)})
        return static

    @register.url('path', '7z')
    def _(self, static: Dict) -> Dict:
        url = self.url_from_path(self.root/static['data'])
        static.update({'type': ['embed', '7z'], 'data': self._urlopen(url)})
        return static

    @register.url('path', 'foam', 'json')
    def _(self, static: Dict) -> Dict:
        return self._path_foam(static)

    @register.url('path', 'foam', 'yaml')
    def _(self, static: Dict) -> Dict:
        return self._path_foam(static)

    def _urlopen(self, url: str) -> bytes:
        with urllib.request.urlopen(url) as f:
            return f.read()

    def _path_foam(self, static: Dict) -> Dict:
        url = self.url_from_path(self.root/static['data'])
        self._foam['foam'][static['name'].split('/')] = {  # p.Path(static['name']).parts
            'json': lambda bytes: json.loads(bytes),
            'yaml': lambda bytes: lib['yaml'].load(bytes, Loader=lib['SafeLoader']),
        }[static['type'][2]](self._urlopen(url))
        static.update({'type': []})
        return static


class YAML:
    '''OpenFOAM YAML parser'''

    _instance = None

    @classmethod
    def default(cls) -> 'Self':
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def data(self, data: Dict) -> t.Iterator[str]:
        for key, value in data.items():
            yield f'{self.key(key)} {self.value(value)}'

    def key(self, key: str) -> str:
        key = key.replace(' ', '')  # div(phi, U) -> div(phi,U)
        if any(c in key for c in '()*|'):  # (U|k|epsilon) -> "(U|k|epsilon)"
            key = f'"{key}"'
        return key

    @f.singledispatchmethod
    def value(self, value: t.Any) -> str:
        raise Exception(f'Unknown type "{type(value).__name__}"')

    @value.register(bool)
    def _(self, value: bool) -> str:
        return f'{str(value).lower()};'

    @value.register(float)
    @value.register(int)
    @value.register(str)
    def _(self, value: t.Union[str, int, float]) -> str:
        return f'{value};'

    @value.register(list)
    def _(self, value: t.List[t.Any]) -> str:
        if not value or isinstance(value[0], (str, int, float)):
            return f'({" ".join(map(str, value))});'
        elif isinstance(value[0], dict):
            strings = []
            for element in value:
                head = tuple(k for k, v in element.items() if v is None)
                if head:
                    element_cloned = element.copy()
                    element_cloned.pop(head[0])
                    string = ' '.join(self.data(element_cloned))
                    strings.append(f'{head[0]} {{{string}}}')
                else:
                    string = ' '.join(self.data(element))
                    strings.append(f'{{{string}}}')
            return f'({" ".join(strings)});'
        else:
            raise Exception(f'Unknown list "{value}"')

    @value.register(dict)
    def _(self, value: Dict) -> str:
        string = ' '.join(self.data(value))
        return f'{{{string}}}'


class Parser:
    '''All parsers'''

    def __init__(self, static: Static, url: Url, yaml: YAML) -> None:
        self.static = static
        self.url = url
        self.yaml = yaml

    @classmethod
    def from_foam(cls, foam: 'Foam') -> 'Self':
        return cls(
            Static.from_foam(foam),
            Url.from_foam(foam),
            YAML.default(),
        )
