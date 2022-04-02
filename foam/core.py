__all__ = ['Foam']


import io
import json
import pathlib as p
import shutil
import typing as t
import warnings

from .command import Command
from .parse import Parse
from .type import Dict, List, Path, Data


class Foam:
    '''Convert multiple dictionary type data to OpenFOAM test case

    Example:
        >>> path = pathlib.Path('tutorials/incompressible/simpleFoam/airFoil2D.yaml')
        >>> foam = Foam.from_file(path)
        >>> foam.meta['openfoam'].append(8)
        >>> foam['foam']['system', 'controlDict', 'endTime'] = 700
        >>> foam.save(path.stem)
        >>> process = foam.cmd.run('./Allrun', output=True)
        >>> print(process)
        Process(code=0, time=7.043395757675171, stdout=b'Running simpleFoam on airFoil2D\n', stderr=b'')
    '''

    __version__ = '0.5.0'

    def __init__(self, data: List, root: Path) -> None:
        from packaging.version import parse

        self.cmd = Command(self)
        self.parse = Parse(self)

        self._list = data
        self._root = p.Path(root)
        self._dest = None

        version = parse(self.__version__)
        current = parse(str(self.meta.get('version', '0.0.0')))
        if version < current:
            warnings.warn('Forward compatibility is not yet guaranteed')
        elif version > current:
            warnings.warn('Backward compatibility is not yet guaranteed')

    def __getitem__(self, key: str) -> t.Optional['Data']:
        try:
            return Data(self._list[self.meta['order'].index(key)])
        except ValueError:
            return None

    def __repr__(self) -> str:
        return f'<Foam @ "{self._root.absolute().as_posix()}">'

    @property
    def meta(self) -> Dict:
        return self._list[0]

    @classmethod
    def from_file(cls, path: Path) -> 'Foam':
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
    def from_json(cls, text: str, root: Path) -> 'Foam':
        data = json.loads(text)
        return cls(data, root)

    @classmethod
    def from_yaml(cls, text: str, root: Path) -> 'Foam':
        import yaml

        try:
            from yaml import CSafeLoader as SafeLoader
        except:
            from yaml import SafeLoader

        data = list(yaml.load_all(text, Loader=SafeLoader))
        return cls(data, root)

    def save(self, dest: Path, paraview: bool = True) -> 'Foam':
        '''Persist case to hard disk'''
        self._dest = p.Path(dest)
        self._dest.mkdir(parents=True, exist_ok=True)
        self._save_foam()
        self._save_static()
        if paraview:
            self._write(self._dest/'paraview.foam', '')
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
            out = self._dest / static['name']  # self._dest is not None
            out.parent.mkdir(parents=True, exist_ok=True)
            out: p.Path
            if static['type'][0] == 'embed':
                if static['type'][1] == 'text':
                    self._write(out, static['data'], static.get('permision', None))
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
            path = self._dest / p.Path(*map(str, keys))  # self._dest is not None
            path.parent.mkdir(parents=True, exist_ok=True)
            self._write(path, '\n'.join(self.parse.data(data)))

    def _extract_files(
        self,
        data: Dict, keys: t.List[str] = [],
    ) -> t.Iterator[t.Tuple[t.List[str], Dict]]:
        if 'FoamFile' in data:
            yield keys, data
        else:
            for key, value in data.items():
                yield from self._extract_files(value, keys+[key])
