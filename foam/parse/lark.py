__all__ = ['Lark']


import os
import pathlib as p
import re
import typing as t

from ..base.lib import lark
from ..base.type import Dict, FoamData, List, Path
from ..compat.functools import cached_property
from ..util.function import grammar
from ..util.implementation import Singleton

if t.TYPE_CHECKING:
    from typing_extensions import Self

    import lark as _lark


class Lark(Singleton):
    '''Lark is a parsing toolkit for Python

    TODO:
        - unit-test (Lark, Foam.from_openfoam)
    '''

    order = ['meta', 'foam', 'static', 'other']

    def __init__(self, path: Path, embed: bool = True) -> None:
        self._root = p.Path(path)
        self._embed = embed
        # foam, static
        self._foam = {}
        self._static = []

    @classmethod
    def from_path(cls, path: Path, **kwargs: t.Any) -> 'Self':
        return cls.new(path, **kwargs)

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

    @cached_property
    def lark(self) -> '_lark.Lark':
        kwargs = {
            'debug': False,
            'cache': False,  # cache only works with parser='lalr' for now
            'parser': 'earley', # or 'lalr'
            'lexer': 'dynamic',  # Parser 'lalr' does not support lexer 'dynamic', expected one of ('basic', 'contextual')
            'transformer': None,
            'start': 'start',
        }
        return lark.Lark(grammar(), **kwargs)

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
        pattern = re.compile(r'^(OpenFOAM-)([\d.x]+)$')
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
