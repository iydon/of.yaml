__all__ = ['Foam']


import functools as f
import gc
import io
import json
import os
import pathlib as p
import shutil
import typing as t
import warnings as w

from .parse import Parser
from .type import Dict, List, Path, Data

if t.TYPE_CHECKING:
    from ..app import Command, Information, PostProcess


class Foam:
    '''Convert multiple dictionary type data to OpenFOAM test case

    Example:
        >>> foam = Foam.from_file('tutorials/incompressible/simpleFoam/airFoil2D.yaml')
        >>> foam['foam']['system', 'controlDict', 'endTime'] = 700
        >>> foam.save('airFoil2D')
        >>> foam.cmd.all_run()
    '''

    __version__ = '0.10.0'

    Self = __qualname__

    def __init__(self, data: List, root: Path) -> None:
        from packaging.version import parse

        self._list = data
        self._root = p.Path(root)
        self._parse = Parser.new()
        self._dest = None

        self._cmd = None
        self._info = None
        self._post = None

        openfoam = set(map(str, self.meta.get('openfoam', [])))
        if str(self.environ['WM_PROJECT_VERSION']) not in openfoam:
            w.warn('OpenFOAM version mismatch')
        version = parse(self.__version__)
        current = parse(str(self.meta.get('version', '0.0.0')))
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

    @property
    def meta(self) -> Dict:
        '''Meta information'''
        return self._list[0]

    @property
    def cmd(self) -> 'Command':
        '''`app.command.Command`'''
        from ..app import Command

        if self._cmd is None:
            self._cmd = Command.from_foam(self)
        return self._cmd

    @property
    def info(self) -> 'Information':
        '''`app.information.Information`'''
        from ..app import Information

        if self._info is None:
            self._info = Information.from_foam(self)
        return self._info

    @property
    def post(self) -> 'PostProcess':
        '''`app.postprocess.PostProcess`'''
        from ..app import PostProcess

        if self._post is None:
            self._post = PostProcess.from_foam(self)
        return self._post

    @f.cached_property
    def application(self) -> str:
        '''Inspired by `getApplication`

        - Reference:
            - foamDictionary -disableFunctionEntries -entry application -value system/controlDict
        '''
        return self['foam']['system', 'controlDict', 'application']

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

    @classmethod
    def from_file(cls, path: Path) -> Self:
        '''Supported format: json, yaml'''
        path = p.Path(path)
        for suffixes, method in [
            ({'.json'}, cls.from_json),
            ({'.yaml', '.yml'}, cls.from_yaml),
        ]:
            if path.suffix in suffixes:
                return method(path.read_text('utf-8'), path.parent)
        raise Exception(f'Suffix "{path.suffix}" not supported')

    @classmethod
    def from_json(cls, text: str, root: Path) -> Self:
        data = json.loads(text)
        return cls(data, root)

    @classmethod
    def from_yaml(cls, text: str, root: Path) -> Self:
        import yaml

        try:
            from yaml import CSafeLoader as SafeLoader
        except:
            from yaml import SafeLoader

        data = list(yaml.load_all(text, Loader=SafeLoader))
        return cls(data, root)

    @classmethod
    def as_placeholder(cls) -> Self:
        return cls([{}], '')

    def save(self, dest: Path, paraview: bool = True) -> Self:
        '''Persist case to hard disk'''
        self._dest = p.Path(dest)
        self._dest.mkdir(parents=True, exist_ok=True)
        self._save_foam()
        self._save_static()
        if paraview:
            self._write(self._dest/'paraview.foam', '')
        return self

    def reset(self) -> Self:
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
        import py7zr

        for static in self['static'] or []:
            # TODO: rewritten as match statement when updated to 3.10
            out = self._path(static['name'])  # self._dest is not None
            out.parent.mkdir(parents=True, exist_ok=True)
            if static['type'][0] == 'embed':
                if static['type'][1] == 'text':
                    self._write(out, static['data'], static.get('permission', None))
                elif static['type'][1] == 'binary':
                    out.write_bytes(static['data'])
                elif static['type'][1] == '7z':
                    with py7zr.SevenZipFile(io.BytesIO(static['data']), mode='r') as z:
                        z.extractall(path=out.parent)
            elif static['type'][0] == 'path':
                in_ = self._root / static['data']
                if static['type'][1] == 'raw':
                    if in_.is_dir():
                        shutil.copytree(in_, out, dirs_exist_ok=True)
                    elif in_.is_file():
                        shutil.copyfile(in_, out)
                    else:
                        raise Exception('Target is neither a file nor a directory')
                elif static['type'][1] == '7z':
                    with py7zr.SevenZipFile(in_, mode='r') as z:
                        z.extractall(path=out.parent)
            else:
                raise Exception(f'Unknown types "{static["type"]}"')

    def _save_foam(self) -> None:
        foam = self['foam']
        for keys, data in self._extract_files({} if foam is None else foam.data):
            path = self._path(*map(str, keys))  # self._dest is not None
            path.parent.mkdir(parents=True, exist_ok=True)
            self._write(path, '\n'.join(self._parse.data(data)))

    def _extract_files(
        self,
        data: Dict, keys: t.List[str] = [],
    ) -> t.Iterator[t.Tuple[t.List[str], Dict]]:
        if 'FoamFile' in data:
            yield keys, data
        else:
            for key, value in data.items():
                yield from self._extract_files(value, keys+[key])

    def _path(self, *parts: str) -> p.Path:
        # TODO: use "prefix" will cause some of the `Command` methods to fail
        prefix = '.'  # (self['other'] or {}).get('directory', '.')
        return self._dest / prefix / p.Path(*parts)
