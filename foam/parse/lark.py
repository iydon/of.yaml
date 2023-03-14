__all__ = ['Lark']


import os
import pathlib as p
import re
import typing as t

from ..base.lib import lark
from ..base.type import DictStrAny, FoamItems, Path
from ..compat.functools import cached_property
from ..util.function import deprecated_classmethod, grammar
from ..util.implementation import Singleton

if t.TYPE_CHECKING:
    import typing_extensions as te

    import lark as _lark

    P = te.ParamSpec('P')
    Kwargs = te.ParamSpecKwargs(P)


class Lark(Singleton):
    '''Lark is a parsing toolkit for Python

    TODO:
        - unit-test (Lark, Foam.fromOpenFoam)
    '''

    __slots__ = ('_root', '_embed', '_foam', '_static')
    order = ['meta', 'foam', 'static', 'other']

    def __init__(self, path: Path, embed: bool = True) -> None:
        self._root = p.Path(path)
        self._embed = embed
        # foam, static
        self._foam = {}
        self._static = []

    @classmethod
    def fromPath(cls, path: Path, **kwargs: 'Kwargs') -> 'te.Self':
        return cls.new(path, **kwargs)

    @property
    def meta(self) -> DictStrAny:
        return {'openfoam': [self._openfoam()], 'version': '0.0.0', 'order': self.order}

    @property
    def foam(self) -> DictStrAny:
        return self._foam

    @property
    def static(self) -> t.List[DictStrAny]:
        return self._static

    @property
    def other(self) -> DictStrAny:
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

    def to_foam_data(self) -> FoamItems:
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

    def _static_item(self, path: p.Path) -> DictStrAny:
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

    from_path = deprecated_classmethod(fromPath)
