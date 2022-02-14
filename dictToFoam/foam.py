__all__ = ['Foam']


import io
import json
import pathlib as p
import shutil
import subprocess
import time
import typing as t
import warnings


Dict = t.Dict[str, t.Any]
List = t.List[Dict]
Path = t.Union[str, p.Path]


class Foam:
    '''Convert multiple dictionary type data to OpenFOAM test case

    Example:
        >>> path = pathlib.Path('tutorials/incompressible/simpleFoam/airFoil2D.yaml')
        >>> foam = Foam.from_file(path)
        >>> foam.meta['openfoam'].append(8)
        >>> foam['foam']['system', 'controlDict', 'endTime'] = 700
        >>> foam.save(path.stem)
        >>> process = foam.run('./Allrun', output=True)
        >>> print(process)
        Process(code=0, time=7.043395757675171, stdout=b'Running simpleFoam on airFoil2D\n', stderr=b'')
    '''

    __version__ = '0.4.0'

    def __init__(self, data: List, root: Path) -> None:
        from packaging.version import parse

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

    def save(self, dest: Path) -> 'Foam':
        '''Persist case to hard disk'''
        self._dest = p.Path(dest)
        self._dest.mkdir(parents=True, exist_ok=True)
        self._save_foam()
        self._save_static()
        return self

    def run(self, command: str, output: bool = True) -> 'Process':
        '''Execute command in case directory'''
        assert self._dest is not None, 'Please call `save` method first'
        now = time.time()
        cp = subprocess.run(command, cwd=self._dest, capture_output=output)
        return Process(
            code=cp.returncode, time=time.time()-now,
            stdout=cp.stdout, stderr=cp.stderr,
        )

    def _write(self, path: p.Path, string: str) -> None:
        with open(path, 'w', encoding='utf-8', newline='\n') as f:  # CRLF -> LF
            f.write(string)

    def _save_static(self) -> None:
        import py7zr

        for static in self['static'] or []:  # 
            # TODO: rewritten as match statement when updated to 3.10
            out = self._dest / static['name']  # self._dest is not None
            out.parent.mkdir(parents=True, exist_ok=True)
            if static['type'][0] == 'embed':
                if static['type'][1] == 'text':
                    self._write(out, static['data'])
                    continue
                elif static['type'][1] == 'binary':
                    out.write_bytes(static['data'])
                    continue
                elif static['type'][1] == '7z':
                    with py7zr.SevenZipFile(io.BytesIO(static['data']), mode='r') as z:
                        z.extractall(path=out.parent)
                    continue
            elif static['type'][0] == 'path':
                in_ = self._root / static['data']
                if static['type'][1] == 'raw':
                    if in_.is_dir():
                        shutil.copytree(in_, out, dirs_exist_ok=True)
                    elif in_.is_file():
                        shutil.copyfile(in_, out)
                    else:
                        raise Exception('Target is neither a file nor a directory')
                    continue
                elif static['type'][1] == '7z':
                    with py7zr.SevenZipFile(in_, mode='r') as z:
                        z.extractall(path=out.parent)
                    continue
            raise Exception(f'Unknown types "{static["type"]}"')

    def _save_foam(self) -> None:
        foam = self['foam']
        for keys, data in self._extract_file_recursively({} if foam is None else foam.data):
            path = self._dest / p.Path(*map(str, keys))  # self._dest is not None
            path.parent.mkdir(parents=True, exist_ok=True)
            self._write(path, '\n'.join(self._convert_dict_recursively(data)))

    def _extract_file_recursively(
        self,
        data: Dict, keys: t.List[str] = [],
    ) -> t.Iterator[t.Tuple[t.List[str], Dict]]:
        if 'FoamFile' in data:
            yield keys, data
        else:
            for key, value in data.items():
                yield from self._extract_file_recursively(value, keys+[key])

    def _convert_dict_recursively(self, data: Dict) -> t.Iterator[str]:
        for key, value in data.items():
            # pre-process
            key = key.replace(' ', '')  # div(phi, U) -> div(phi,U)
            if any(c in key for c in '()*'):  # (U|k|epsilon) -> "(U|k|epsilon)"
                key = f'"{key}"'
            # TODO: rewritten as match statement when updated to 3.10
            if isinstance(value, bool):  # bool < int
                yield f'{key} {str(value).lower()};'
            elif isinstance(value, (str, int, float)):
                yield f'{key} {value};'
            elif isinstance(value, list):
                if not value or isinstance(value[0], (str, int, float)):
                    yield f'{key} ({" ".join(map(str, value))});'
                elif isinstance(value[0], dict):
                    strings = []
                    for element in value:
                        head = tuple(k for k, v in element.items() if v is None)
                        if head:
                            element.pop(head[0])
                            string = ' '.join(self._convert_dict_recursively(element))
                            strings.append(f'{head[0]} {{{string}}}')
                        else:
                            string = ' '.join(self._convert_dict_recursively(element))
                            strings.append(f'{{{string}}}')
                    yield f'{key} ({" ".join(strings)});'
                else:
                    raise Exception(f'Unknown list "{value}"')
            elif isinstance(value, dict):
                string = ' '.join(self._convert_dict_recursively(value))
                yield f'{key} {{{string}}}'
            else:
                raise Exception(f'Unknown type "{type(value).__name__}"')


class Data:
    def __init__(self, data: t.Union[Dict, List]) -> None:
        self._data = data

    def __getitem__(self, keys: t.Any) -> t.Any:
        if isinstance(keys, tuple):
            ans = self._data
            for key in keys:
                ans = ans[key]
            return ans
        else:
            return self._data[keys]

    def __setitem__(self, keys: t.Any, value: t.Any) -> None:
        if isinstance(keys, tuple):
            assert keys
            ans = self._data
            for key in keys[:-1]:
                if isinstance(ans, dict):
                    ans = ans.setdefault(key, {})
                elif isinstance(ans, list):
                    ans = ans[key]
                else:
                    raise Exception
            ans[keys[-1]] = value
        else:
            self._data[keys] = value

    def __bool__(self) -> bool:
        return bool(self._data)  # 'list' object has no attribute '__bool__'

    def __iter__(self) -> t.Iterator[t.Any]:
        return self._data.__iter__()

    def __repr__(self) -> str:
        return self._data.__repr__()

    @property
    def data(self) -> t.Union[Dict, List]:
        return self._data


class Process(t.NamedTuple):
    # args: str  # does this field need to be deleted?
    code: int
    time: float
    stdout: t.Optional[bytes] = None
    stderr: t.Optional[bytes] = None
