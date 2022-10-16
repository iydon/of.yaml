__all__ = ['Lark']


import functools as f
import os
import pathlib as p
import re
import typing as t

import lark  # TODO: lib.lark

from ..base.type import Dict, FoamData, List, Path

if t.TYPE_CHECKING:
    from typing_extensions import Self


class Lark:
    '''Lark is a parsing toolkit for Python'''

    __grammar__ = p.Path(__file__).parents[1] / 'static' / 'grammar' / 'openfoam.lark'

    order = ['meta', 'foam', 'static', 'other']

    _instance = None

    def __init__(self, path: Path, embed: bool = True) -> None:
        self._root = p.Path(path)
        self._embed = embed
        # foam, static
        self._foam = {}
        self._static = []

    @classmethod
    def from_path(cls, path: Path, **kwargs: t.Any) -> 'Self':
        if cls._instance is None:
            cls._instance = cls(path, **kwargs)
        return cls._instance

    @property
    def meta(self) -> Dict:
        return {'openfoam': [self._openfoam()], 'version': '0.0.0', 'order': self.order}

    @property
    def foam(self) -> Dict:
        return self._foam

    @property
    def static(self) -> List:
        return self._static

    @property
    def other(self) -> Dict:
        return {'pipeline': []}

    @f.cached_property
    def lark(self) -> lark.Lark:
        kwargs = {
            'debug': False,
            'parser': 'earley',
            'lexer': 'auto',
            'transformer': None,
            'start': 'start',
        }
        return lark.Lark(self.__grammar__.read_text(), **kwargs)

    def parse(self) -> None:
        for path in self._root.rglob('*'):
            if path.is_file():
                # TODO: foam part
                self._static.append(self._static_item(path))

    def parse_once(self) -> None:
        '''#pragma once'''
        if not self.parsed():
            self.parse()

    def parsed(self) -> bool:
        return bool(self._foam) or bool(self._static)

    def to_foam_data(self) -> FoamData:
        self.parse_once()
        return [getattr(self, o) for o in self.order]

    def _openfoam(self) -> str:
        '''OpenFOAM Version'''
        pattern = re.compile(r'^(OpenFOAM-)([\d\.x]+)$')
        for part in self._root.parts:
            match = pattern.match(part)
            if match is not None:
                return match.groups()[-1]
        return os.environ['WM_PROJECT_VERSION']

    def _static_item(self, path: p.Path) -> Dict:
        name = path.relative_to(self._root).as_posix()
        permission = oct(path.stat().st_mode)[-3:]
        if self._embed:
            data = path.read_bytes()
            try:
                data = data.decode()
            except UnicodeDecodeError:
                type = ['embed', 'binary']
            else:
                type = ['embed', 'text']
        else:
            data = path.as_posix()
            type = ['path', 'raw']
        return {'name': name, 'type': type, 'permission': permission, 'data': data}