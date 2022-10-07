__all__ = ['Foam']


import functools as f
import gc
import json
import os
import pathlib as p
import typing as t
import urllib
import warnings as w

from .lib import lib
from .parse import Parser
from .type import Dict, List, Path, Data, Version

if t.TYPE_CHECKING:
    from typing_extensions import Self

    from ..app.command.core import Command
    from ..app.information.core import Information
    from ..app.postprocess.core import PostProcess


class Foam:
    '''Convert multiple dictionary type data to OpenFOAM test case

    Example:
        >>> foam = Foam.from_demo('cavity')
        >>> foam['foam']['system', 'controlDict', 'endTime'] = 1.0
        >>> foam.save('cavity')
        >>> foam.cmd.all_run()
    '''

    __version__ = '0.11.9'

    def __init__(self, data: List, root: Path, warn: bool = True) -> None:
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
            version = Version.from_string(self.__version__)
            current = Version.from_string(str(self.meta.get('version', '0.0.0')))
            if (version.major, version.minor) < (current.major, current.minor):
                w.warn('Forward compatibility is not yet guaranteed')
            elif (version.major, version.minor) > (current.major, current.minor):
                w.warn('Backward compatibility is not yet guaranteed')

    def __getitem__(self, key: str) -> t.Optional['Data']:
        try:
            return Data(self._list[self.meta['order'].index(key)])
        except ValueError:
            return None

    def __repr__(self) -> str:
        return f'<Foam @ "{self._root.absolute().as_posix()}">'

    @classmethod
    def list_demos(cls) -> t.List[str]:
        root = p.Path(__file__).parents[1] / 'demo' / os.environ['WM_PROJECT_VERSION']
        return sorted(
            path.stem
            for path in root.iterdir()
            if path.suffix == '.yaml'
        )

    @classmethod
    def from_demo(cls, name: str = 'cavity') -> 'Self':
        version = os.environ['WM_PROJECT_VERSION']
        name = name if name.endswith('.yaml') else f'{name}.yaml'
        path = p.Path(__file__).parents[1] / 'demo' / version / name
        try:
            self = cls.from_file(path, warn=False)
        except FileNotFoundError:
            raise FileNotFoundError(f'No such demo: "{name[:-5]}" not in {cls.list_demos()}')
        else:
            print(f'Foam.from_file(\'{path.as_posix()}\', warn=False)')
            self.meta.setdefault('openfoam', []).append(version)
            self.meta['version'] = cls.__version__
            return self

    @classmethod
    def from_demos(cls) -> t.List['Self']:
        return list(map(cls.from_demo, cls.list_demos()))

    @classmethod
    def from_remote_file(cls, url: str, **kwargs: t.Any) -> 'Self':
        with urllib.request.urlopen(url) as f:
            text = f.read()
        split_url = urllib.parse.urlsplit(url)
        path = p.Path(split_url.path)
        self = cls.from_text(text, '.', path.suffix, **kwargs)
        self.parser.url.set_split_url(split_url)
        for old in self['static'] or []:
            types = tuple(old.get('type', []))
            old.update(self.parser.url[types](old.copy()))
        return self

    @classmethod
    def from_file(cls, path: Path, **kwargs: t.Any) -> 'Self':
        '''Supported format: json, yaml'''
        path = p.Path(path)
        return cls.from_text(path.read_text(), path.parent, path.suffix, **kwargs)

    @classmethod
    def from_text(cls, text: str, root: Path, suffix: t.Optional[str] = None, **kwargs: t.Any) -> 'Self':
        mapper = [
            ({'.json'}, cls.from_json),
            ({'.yaml', '.yml'}, cls.from_yaml),
        ]
        if suffix is not None:
            for suffixes, method in mapper:
                if suffix in suffixes:
                    return method(text, root, **kwargs)
        else:
            for _, method in mapper:
                try:
                    return method(text, root, **kwargs)
                except Exception as e:
                    print(method.__name__, e)
        raise Exception(f'Suffix "{suffix}" is not supported or not recognized')

    @classmethod
    def from_json(cls, text: str, root: Path, **kwargs: t.Any) -> 'Self':
        data = json.loads(text)
        return cls(data, root, **kwargs)

    @classmethod
    def from_yaml(cls, text: str, root: Path, **kwargs: t.Any) -> 'Self':
        data = list(lib['yaml'].load_all(text, Loader=lib['SafeLoader']))
        return cls(data, root, **kwargs)

    @classmethod
    def as_placeholder(cls) -> 'Self':
        return cls([{}], '', warn=False)

    @property
    def meta(self) -> Dict:
        '''Meta information'''
        return self._list[0]

    @property
    def parser(self) -> Parser:
        '''All parsers'''
        if self._parser is None:
            self._parser = Parser.from_foam(self)
        return self._parser

    @property
    def cmd(self) -> 'Command':
        '''`app.command.Command`'''
        from ..app.command.core import Command

        if self._cmd is None:
            self._cmd = Command.from_foam(self)
        return self._cmd

    @property
    def info(self) -> 'Information':
        '''`app.information.Information`'''
        from ..app.information.core import Information

        if self._info is None:
            self._info = Information.from_foam(self)
        return self._info

    @property
    def post(self) -> 'PostProcess':
        '''`app.postprocess.PostProcess`'''
        from ..app.postprocess.core import PostProcess

        if self._post is None:
            self._post = PostProcess.from_foam(self)
        return self._post

    @f.cached_property
    def application(self) -> str:
        '''Inspired by `getApplication`

        - Reference:
            - foamDictionary -disableFunctionEntries -entry application -value system/controlDict
        '''
        for key, value in self['foam']['system', 'controlDict'].items():
            if key.startswith('application'):
                return value
        raise Exception('Application not found')

    @f.cached_property
    def number_of_processors(self) -> int:
        '''Inspired by `getNumberOfProcessors`

        - Reference:
            - foamDictionary -disableFunctionEntries -entry numberOfSubdomains -value system/decomposeParDict
        '''
        try:
            return self['foam']['system', 'decomposeParDict', 'numberOfSubdomains']
        except:
            return 1

    @f.cached_property
    def pipeline(self) -> t.List[t.Union[str, t.Dict[str, t.Any]]]:
        return (self['other'] or {}).get('pipeline', [])

    @f.cached_property
    def environ(self) -> t.Dict[str, str]:
        '''OpenFOAM environments'''
        return {
            key: value
            for key, value in os.environ.items()
            if any(key.startswith(p) for p in ['FOAM_', 'WM_'])
        }

    @f.cached_property
    def fields(self) -> t.Set[str]:
        return {v['FoamFile']['object'] for v in self['foam']['0'].values()}

    @f.cached_property
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
            self._write(path, '\n'.join(self.parser.yaml.data(data)))

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
        return self._dest / prefix / p.Path(*parts)
