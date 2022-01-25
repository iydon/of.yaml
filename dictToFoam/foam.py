__all__ = ['Foam']


import io
import json
import pathlib as p
import shutil
import typing as t
import warnings


Dict = t.Dict[str, t.Any]
List = t.List[Dict]
Path = t.Union[str, p.Path]


class Foam:
    '''Convert multiple dictionary type data to OpenFOAM test case'''

    __version__ = '0.4.0'

    def __init__(self, data: List, root: Path) -> None:
        from packaging.version import parse

        self._list = data
        self._root = p.Path(root)

        version = parse(self.__version__)
        current = parse(str(self.meta.get('version', '0.0.0')))
        if version < current:
            warnings.warn('Forward compatibility is not yet guaranteed')
        elif version > current:
            warnings.warn('Backward compatibility is not yet guaranteed')

    def __getitem__(self, key: str) -> t.Optional[Dict]:
        try:
            return self._list[self.meta['order'].index(key)]
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

    def save(self, dest: Path) -> None:
        dest = p.Path(dest)
        dest.mkdir(parents=True, exist_ok=True)
        self._save_foam(dest)
        self._save_static(dest)

    def _write(self, path: p.Path, string: str) -> None:
        with open(path, 'w', encoding='utf-8', newline='\n') as f:  # CRLF -> LF
            f.write(string)

    def _save_static(self, dest: p.Path) -> None:
        import py7zr

        for static in self['static'] or []:
            # TODO: rewritten as match statement when updated to 3.10
            out = dest / static['name']
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

    def _save_foam(self, dest: p.Path) -> None:
        for keys, data in self._extract_file_recursively(self['foam'] or {}):
            path = dest / p.Path(*map(str, keys))
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