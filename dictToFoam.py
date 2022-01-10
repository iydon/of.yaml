import json
import pathlib as p
import shutil
import typing as t

import py7zr
import yaml


Dict = t.Dict[str, t.Any]


class Foam:
    '''Convert dictionary type data to OpenFOAM test case'''
    def __init__(self, data: Dict, root: p.Path, dest: p.Path) -> None:
        self._dict = data
        self._root = root
        self._dest = dest

    def __repr__(self) -> str:
        return f'<Foam @ "{self._root.absolute().as_posix()}">'

    @property
    def data(self) -> Dict:
        return self._dict['data']

    @property
    def meta(self) -> Dict:
        return self._dict['meta']

    @classmethod
    def from_(
        cls,
        path: p.Path, dest: t.Optional[p.Path] = None,
    ) -> 'Foam':
        '''Supported format: json, yaml'''
        for suffixes, method in [
            ({'.json'}, lambda text: json.lodas(text)),
            ({'.yaml', '.yml'}, lambda text: yaml.load(text, Loader=yaml.SafeLoader))
        ]:
            if path.suffix in suffixes:
                data = method(path.read_text('utf-8'))
                return cls(data, path.parent, dest or path.parent/path.stem)
        raise Exception(f'Suffix "{path.suffix}" not supported')

    def save(self) -> None:
        self._dest.mkdir(parents=True, exist_ok=True)
        self._save_static()
        self._save_data()

    def _write(self, path: p.Path, string: str) -> None:
        with open(path, 'w', encoding='utf-8', newline='\n') as f:  # CRLF -> LF
            f.write(string)

    def _save_static(self) -> None:
        for static in self.meta.get('static', []):
            # TODO: rewritten as match statement when updated to 3.10
            in_ = self._root / static['data']
            out = self._dest / static['name']
            out.parent.mkdir(parents=True, exist_ok=True)
            if static['type'] == 'text':
                self._write(out, static['data'])
            elif static['type'] == 'path':
                if in_.is_dir():
                    shutil.copytree(in_, out, dirs_exist_ok=True)
                elif in_.is_file():
                    shutil.copyfile(in_, out)
                else:
                    raise Exception('Target is neither a file nor a directory')
            elif static['type'] == '7z':
                with py7zr.SevenZipFile(in_, mode='r') as z:
                    z.extractall(path=out.parent)
            else:
                raise Exception(f'Unknown type "{static["type"]}"')

    def _save_data(self) -> None:
        global data
        for keys, data in self._extract_file_recursively(self.data):
            path = self._dest / p.Path(*map(str, keys))
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
            key = key.replace(' ', '')  # div(phi, U) -> div(phi,U)
            # TODO: rewritten as match statement when updated to 3.10
            if isinstance(value, bool):  # bool < int
                yield f'{key} {str(value).lower()}'
            if isinstance(value, (str, int, float)):
                yield f'{key} {value};'
            elif isinstance(value, dict):
                string = ' '.join(self._convert_dict_recursively(value))
                yield f'{key} {{{string}}}'
            else:
                raise Exception(f'Unknown type "{type(value).__name__}"')
