__all__ = ['Static']


import io
import pathlib as p
import shutil
import typing as t

from ..base.lib import py7zr
from ..base.type import Dict, Keys
from ..util.decorator import Match
from ..util.object.conversion import Conversion
from ..util.object.data import Data

if t.TYPE_CHECKING:
    from typing_extensions import Self

    from ..base.core import Foam


class Static:
    '''OpenFOAM static parser

    Example:
        >>> foam = Foam.from_demo('cavity')
        Foam.from_path('.../of.yaml/foam/static/demo/7/cavity.yaml', warn=False)
        >>> foam.save('case')

        >>> data = {
        ...     'name': 'Allrun',
        ...     'type': ['embed', 'text'],
        ...     'permission': 777,
        ...     'data': 'echo hello world!\n',
        ... }
        >>> static = Static.from_foam(foam)
        >>> static[tuple(data['type'])](data)
    '''

    match = Match.default()

    def __init__(self, foam: 'Foam') -> None:
        self._foam = foam

    def __getitem__(self, keys: Keys[str]) -> t.Callable:
        try:
            return lambda *args, **kwargs: self.match[keys](self, *args, **kwargs)
        except KeyError:
            raise Exception(f'Unknown types "{keys}"')

    @classmethod
    def from_foam(cls, foam: 'Foam') -> 'Self':
        return cls(foam)

    @match.register()
    def _(self, static: Dict) -> None:
        # do nothing
        pass

    @match.register('embed', 'text')
    def _(self, static: Dict) -> None:
        out = self._out(static['name'])
        self._foam._write(out, static['data'], static.get('permission', None))

    @match.register('embed', 'binary')
    def _(self, static: Dict) -> None:
        out = self._out(static['name'])
        out.write_bytes(static['data'])

    @match.register('embed', '7z')
    def _(self, static: Dict) -> None:
        out = self._out(static['name'])
        with py7zr.SevenZipFile(io.BytesIO(static['data']), mode='r') as z:
            z.extractall(path=out.parent)

    @match.register('path', 'raw')
    def _(self, static: Dict) -> None:
        out, in_ = self._out(static['name']), self._in(static['data'])
        if in_.is_dir():
            shutil.copytree(in_, out, dirs_exist_ok=True)
        elif in_.is_file():
            shutil.copyfile(in_, out)
        else:
            raise Exception('Target is neither a file nor a directory')

    @match.register('path', '7z')
    def _(self, static: Dict) -> None:
        out, in_ = self._out(static['name']), self._in(static['data'])
        with py7zr.SevenZipFile(in_, mode='r') as z:
            z.extractall(path=out.parent)

    @match.register('path', 'foam', 'json')
    def _(self, static: Dict) -> None:
        self._path_foam(static)

    @match.register('path', 'foam', 'toml')
    def _(self, static: Dict) -> None:
        self._path_foam(static)

    @match.register('path', 'foam', 'yaml')
    def _(self, static: Dict) -> None:
        self._path_foam(static)

    def _out(self, name: str) -> p.Path:
        out = self._foam._path(name)
        out.parent.mkdir(parents=True, exist_ok=True)
        return out

    def _in(self, data: str) -> p.Path:
        return self._foam._root / data

    def _path_foam(self, static: Dict) -> None:
        data = Data.from_dict()
        out, in_ = self._foam._path(), self._in(static['data'])
        data[static['name'].split('/')] = Conversion \
            .from_bytes(in_.read_bytes(), static['type'][2], all=False) \
            .to_document()
        self._foam.__class__([{'order': ['meta', 'foam']}, data._data], in_.parent, warn=False) \
            .save(out, paraview=False)
