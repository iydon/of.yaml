__all__ = ['Foam']


import copy
import functools as f
import gc
import os
import pathlib as p
import shutil
import typing as t
import urllib.parse
import urllib.request
import warnings as w

from .type import Dict, FoamData, Path
from ..compat.functools import cached_property
from ..parse import Parser
from ..util.function import deprecated_classmethod
from ..util.object.conversion import Conversion
from ..util.object.data import Data
from ..util.object.version import Version

if t.TYPE_CHECKING:
    from typing_extensions import Self

    from ..app.command.core import Command
    from ..app.information.core import Information
    from ..app.postprocess.core import PostProcess


class Foam:
    '''Convert multiple dictionary type data to OpenFOAM test case

    Example:
        >>> foam = Foam.fromRemoteDemo('cavity')
        >>> foam['foam']['system', 'controlDict', 'endTime'] = 1.0
        >>> foam.save('cavity')
        >>> foam.cmd.all_run()
    '''

    __version__ = Version.fromString('0.13.4')

    def __init__(self, data: FoamData, root: Path, warn: bool = True) -> None:
        self._list = data
        self._root = p.Path(root)
        self._dest: t.Optional[p.Path] = None

        self._parser: t.Optional[Parser] = None
        self._cmd: t.Optional['Command'] = None
        self._info: t.Optional['Information'] = None
        self._post: t.Optional['PostProcess'] = None

        if warn:
            openfoam = set(map(str, self.meta.get('openfoam', [])))
            if str(self.environ['WM_PROJECT_VERSION']) not in openfoam:
                w.warn(f'OpenFOAM version mismatch: {root}')
            version = Version.fromString(str(self.meta.get('version', '0.0.0')))
            if self.__version__ < version:
                w.warn('Forward compatibility is not yet guaranteed')
            elif self.__version__ > version:
                w.warn('Backward compatibility is not yet guaranteed')

    def __getitem__(self, key: str) -> t.Optional[Data]:
        try:
            return Data.fromAny(self._list[self.meta['order'].index(key)])
        except ValueError:
            return None

    def __repr__(self) -> str:
        return f'Foam({self._list!r}, {self._root!r})'

    def __str__(self) -> str:
        return f'<Foam @ "{self._root.absolute().as_posix()}">'

    @classmethod
    def listDemos(cls) -> t.List[str]:
        root = p.Path(__file__).parents[1] / 'static' / 'demo' / os.environ['WM_PROJECT_VERSION']
        return sorted(
            path.stem
            for path in root.iterdir()
            if path.suffix == '.yaml'
        )

    @classmethod
    def fromDemo(cls, name: str = 'cavity', warn: bool = False, verbose: bool = True) -> 'Self':
        version = os.environ['WM_PROJECT_VERSION']
        name = name if name.endswith('.yaml') else f'{name}.yaml'
        path = p.Path(__file__).parents[1] / 'static' / 'demo' / version / name
        try:
            self = cls.fromPath(path, warn=warn)
        except FileNotFoundError:
            raise FileNotFoundError(f'No such demo: "{name[:-5]}" not in {cls.listDemos()}')
        else:
            if verbose:
                print(f'Foam.fromPath(\'{path.as_posix()}\', warn={warn})')
            self.meta.setdefault('openfoam', []).append(version)
            self.meta['version'] = cls.__version__.to_string()
            return self

    @classmethod
    def fromDemos(cls, warn: bool = False, verbose: bool = True) -> t.List['Self']:
        return list(map(lambda name: cls.fromDemo(name, warn, verbose), cls.listDemos()))

    @classmethod
    def fromRemoteDemo(cls, name: str = 'cavity', timeout: t.Optional[float] = None, warn: bool = False, verbose: bool = True) -> 'Self':
        version = os.environ['WM_PROJECT_VERSION']
        name = name if name.endswith('.yaml') else f'{name}.yaml'
        url = f'https://raw.githubusercontent.com/iydon/of.yaml/main/foam/static/demo/{version}/{name}'
        try:
            self = cls.fromRemotePath(url, timeout, warn=warn)
        except Exception:  # urllib.error.URLError
            raise FileNotFoundError(f'No such demo: "{url}"')
        else:
            if verbose:
                print(f'Foam.fromRemotePath(\'{url}\', warn={warn})')
            self.meta.setdefault('openfoam', []).append(version)
            self.meta['version'] = cls.__version__.to_string()
            return self

    @classmethod
    def fromRemoteDemos(cls, timeout: t.Optional[float] = None, warn: bool = False, verbose: bool = True) -> t.List['Self']:
        return list(map(lambda name: cls.fromRemoteDemo(name, timeout, warn, verbose), cls.listDemos()))

    @classmethod
    def fromRemotePath(cls, url: str, timeout: t.Optional[float] = None, warn: bool = True, type:  t.Optional[str] = None) -> 'Self':
        with urllib.request.urlopen(url, timeout=timeout) as f:
            text = f.read()
        split_url = urllib.parse.urlsplit(url)
        path = p.Path(split_url.path)
        type_or_suffix = path.suffix if type is None else type  # type or path.suffix
        self = cls.fromText(text, '.', type_or_suffix, warn=warn)
        self.parser.url.set_split_url(split_url)
        for old in self['static'] or []:
            types = tuple(old.get('type', []))
            old.update(self.parser.url[types](old.copy()))
        return self

    @classmethod
    def fromPath(cls, path: Path, warn: bool = True, type: t.Optional[str] = None) -> 'Self':
        '''Supported path mode: file, directory'''
        path = p.Path(path)
        if path.is_file():
            type_or_suffix = path.suffix if type is None else type  # type or path.suffix
            return cls.fromText(path.read_text(), path.parent, type_or_suffix, warn=warn)
        elif path.is_dir():
            return cls.fromOpenFoam(path)
        else:
            raise Exception(f'Mode "{path.stat().st_mode}" is not supported')

    @classmethod
    def fromOpenFoam(cls, path: Path, **kwargs: t.Any) -> 'Self':
        '''From OpenFOAM directory'''
        return Parser.toFoam(path, **kwargs)

    @classmethod
    def fromText(
        cls,
        text: t.Union[bytes, str], root: Path,
        type_or_suffix: t.Optional[str] = None, warn: bool = True,
    ) -> 'Self':
        '''Supported formats: please refer to `Conversion`'''
        content = text if isinstance(text, bytes) else text.encode()
        if type_or_suffix is not None:
            data = Conversion.fromBytes(content, type_or_suffix, all=True).to_document()
        else:
            data = Conversion.autoFromBytes(content, all=True).to_document()
        return cls(data, root, warn=warn)

    @classmethod
    def fromYAML(cls, text: str, root: Path, warn: bool = True) -> 'Self':
        data = Conversion.fromString(text, 'yaml', all=True).to_document()
        return cls(data, root, warn=warn)

    @classmethod
    def default(cls) -> 'Self':
        return cls([{}], '', warn=False)

    @property
    def data(self) -> Data:
        return Data.fromList(self._list)

    @property
    def meta(self) -> Data:
        '''Meta information'''
        return Data.fromDict(self._list[0])

    @property
    def parser(self) -> Parser:
        '''All parsers'''
        if self._parser is None:
            self._parser = Parser.fromFoam(self)
        return self._parser

    @property
    def cmd(self) -> 'Command':
        '''`app.command.Command`'''
        from ..app.command.core import Command

        if self._cmd is None:
            self._cmd = Command.fromFoam(self)
        return self._cmd

    @property
    def info(self) -> 'Information':
        '''`app.information.Information`'''
        from ..app.information.core import Information

        if self._info is None:
            self._info = Information.fromFoam(self)
        return self._info

    @property
    def post(self) -> 'PostProcess':
        '''`app.postprocess.PostProcess`'''
        from ..app.postprocess.core import PostProcess

        if self._post is None:
            self._post = PostProcess.fromFoam(self)
        return self._post

    @property
    def destination(self) -> p.Path:
        assert self._dest is not None, 'Please call `Foam::save` method first'

        return self._dest

    @destination.setter
    def destination(self, dest: Path) -> None:
        self._dest = p.Path(dest)

    @destination.deleter
    def destination(self) -> None:
        shutil.rmtree(self.destination)
        self._dest = None

    @cached_property
    def application(self) -> str:
        '''Inspired by `getApplication`

        Reference:
            - foamDictionary -disableFunctionEntries -entry application -value system/controlDict
        '''
        for key, value in self['foam']['system', 'controlDict'].items():
            if key.startswith('application'):
                return value
        raise Exception('Application not found')

    @cached_property
    def number_of_processors(self) -> int:
        '''Inspired by `getNumberOfProcessors`

        Reference:
            - foamDictionary -disableFunctionEntries -entry numberOfSubdomains -value system/decomposeParDict
        '''
        try:
            return self['foam']['system', 'decomposeParDict', 'numberOfSubdomains']
        except Exception:
            return 1

    @cached_property
    def pipeline(self) -> t.List[t.Union[str, Dict]]:
        return (self['other'] or {}).get('pipeline', [])

    @cached_property
    def environ(self) -> t.Dict[str, str]:
        '''OpenFOAM environments'''
        return {
            key: value
            for key, value in os.environ.items()
            if any(key.startswith(p) for p in ['FOAM_', 'WM_'])
        }

    @cached_property
    def fields(self) -> t.Set[str]:
        return {v['FoamFile']['object'] for v in self['foam']['0'].values()}

    @cached_property
    def ndim(self) -> t.Optional[int]:
        # TODO: verify that this method is reliable
        system = self['foam']['system']
        block_mesh = system.get('blockMeshDict', None)
        if block_mesh is None:
            return None  # unknown ndim
        count = 3
        for block in block_mesh['blocks']:
            start = block.find(')')
            if start < 0:
                return None
            begin, end = block.find('(', start+1), block.find(')', start+1)
            if begin < 0 or end < 0:
                return None
            grids = block[begin+1: end].split()
            count = min(count, len(grids)-grids.count('1'))
        return count

    def copy(self) -> 'Self':
        other = self.__class__(copy.deepcopy(self._list), self._root)
        other._dest = self._dest
        return other

    def save(self, dest: Path, paraview: bool = True) -> 'Self':
        '''Persist case to hard disk'''
        self._dest = p.Path(dest)
        self._dest.mkdir(parents=True, exist_ok=True)
        self._save_foam()
        self._save_static()
        if paraview:
            self._write(self._dest/'paraview.foam', '')
        return self

    def reset(self) -> 'Self':
        self._dest = self._cmd = self._info = self._post = None
        for obj in gc.get_objects():
            if isinstance(obj, f._lru_cache_wrapper):
                obj.cache_clear()
        return self

    def _write(self, path: p.Path, string: str, permission: t.Optional[int] = None) -> None:
        with open(path, 'w', encoding='utf-8', newline='\n') as f:  # CRLF -> LF
            f.write(string)
        if permission is not None:
            path.chmod(int(str(permission), base=8))

    def _save_static(self) -> None:
        # TODO: add to parse sub-module
        for static in self['static'] or []:
            self.parser.static[tuple(static['type'])](static)

    def _save_foam(self) -> None:
        foam = self['foam']
        for keys, data in self._extract_files({} if foam is None else foam.data):
            # pre-process FoamFile to avoid duplicate descriptions (not recommended yet)
            if data['FoamFile'] is None:
                data.pop('FoamFile')
            elif isinstance(data['FoamFile'], str):
                data['FoamFile'] = {'class': data['FoamFile']}
            if 'FoamFile' in data:
                for key, value in [('version', 2.0), ('format', 'ascii'), ('object', keys[-1])]:
                    data['FoamFile'].setdefault(key, value)
            # write the parsed text data
            path = self._path(*map(str, keys))  # self._dest is not None
            path.parent.mkdir(parents=True, exist_ok=True)
            self._write(path, '\n'.join(self.parser.case.data(data)))

    def _extract_files(
        self,
        data: Dict, keys: t.List[str] = [],
    ) -> t.Iterator[t.Tuple[t.List[str], Dict]]:
        if 'FoamFile' in data:
            yield keys, data.copy()
        else:
            for key, value in data.items():
                yield from self._extract_files(value, keys+[key])

    def _path(self, *parts: str) -> p.Path:
        # TODO: use "prefix" will cause some of the `Command` methods to fail
        prefix = '.'  # (self['other'] or {}).get('directory', '.')
        return self.destination / prefix / p.Path(*parts)

    list_demos = deprecated_classmethod(listDemos)
    from_demo = deprecated_classmethod(fromDemo)
    from_demos = deprecated_classmethod(fromDemos)
    from_remote_demo = deprecated_classmethod(fromRemoteDemo)
    from_remote_demos = deprecated_classmethod(fromRemoteDemos)
    from_remote_path = deprecated_classmethod(fromRemotePath)
    from_path = deprecated_classmethod(fromPath)
    from_openfoam = deprecated_classmethod(fromOpenFoam, 'from_openfoam')
    from_text = deprecated_classmethod(fromText)
    from_yaml = deprecated_classmethod(fromYAML, 'from_yaml')
