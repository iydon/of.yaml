__all__ = ['Lark']


import pathlib as p
import typing as t

import lark  # TODO: lib.lark

from ..base.type import Dict, FoamData, List, Path

if t.TYPE_CHECKING:
    from typing_extensions import Self


class Lark:
    '''Lark is a parsing toolkit for Python'''

    def __init__(self, path: Path) -> None:
        self._path = p.Path(path)

    @classmethod
    def from_path(cls, path: Path) -> 'Self':
        return cls(path)

    def to_foam_data(self) -> FoamData:
        return [self._meta(), self._foam(), self._static(), self._other()]

    def _meta(self) -> Dict:
        return {'openfoam': [], 'version': '0.0.0', 'order': ['meta', 'foam', 'static', 'other']}

    def _foam(self) -> Dict:
        return {}

    def _static(self) -> List:
        return []

    def _other(self) -> Dict:
        return {'pipeline': []}
