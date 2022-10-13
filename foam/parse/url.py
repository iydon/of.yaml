__all__ = ['Url']


import json
import pathlib as p
import typing as t
import urllib.parse
import urllib.request

from ..base.lib import yaml
from ..base.type import Dict, Keys
from ..util.decorator import Match

if t.TYPE_CHECKING:
    from typing_extensions import Self

    from ..base.core import Foam


class Url:
    '''Merge remote multiple files into a single file

    Example:
        >>> foam = Foam.from_demo('cavity')
        Foam.from_file('.../of.yaml/foam/static/demo/7/cavity.yaml', warn=False)
        >>> foam.save('case')

        >>> data = {
        ...     'name': 'constant/polyMesh',
        ...     'type': ['path', '7z'],
        ...     'permission': None,
        ...     'data': 'static/airFoil2D-polyMesh.7z',
        ... }
        >>> url = Url.from_foam(foam)
        >>> url.set_url('https://raw.githubusercontent.com/iydon/of.yaml-tutorial/main/tutorials/7/incompressible/simpleFoam/airFoil2D.yaml')
        >>> url[tuple(data['type'])](data)
        {'name': 'constant/polyMesh',
         'type': ['embed', '7z'],
         'permission': None,
         'data': ...}
    '''

    match = Match.default()

    def __init__(self, foam: 'Foam') -> None:
        self._foam = foam
        self._path = None
        self._url = None

    def __getitem__(self, keys: Keys[str]) -> t.Callable:
        if not isinstance(keys, tuple):
            keys = (keys, )
        method = self.match.get(*keys, default=lambda self, static: static)
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

    @match.register('path', 'raw')
    def _(self, static: Dict) -> Dict:
        # TODO: directory
        url = self.url_from_path(self.root/static['data'])
        static.update({'type': ['embed', 'binary'], 'data': self._urlopen(url)})
        return static

    @match.register('path', '7z')
    def _(self, static: Dict) -> Dict:
        url = self.url_from_path(self.root/static['data'])
        static.update({'type': ['embed', '7z'], 'data': self._urlopen(url)})
        return static

    @match.register('path', 'foam', 'json')
    def _(self, static: Dict) -> Dict:
        return self._path_foam(static)

    @match.register('path', 'foam', 'yaml')
    def _(self, static: Dict) -> Dict:
        return self._path_foam(static)

    def _urlopen(self, url: str) -> bytes:
        with urllib.request.urlopen(url) as f:
            return f.read()

    def _path_foam(self, static: Dict) -> Dict:
        url = self.url_from_path(self.root/static['data'])
        self._foam['foam'][static['name'].split('/')] = {  # p.Path(static['name']).parts
            'json': lambda bytes: json.loads(bytes),
            'yaml': lambda bytes: yaml.load(bytes),
        }[static['type'][2]](self._urlopen(url))
        static.update({'type': []})
        return static
