__all__ = ['Parser']


import typing as t

from .case import Case
from .lark import Lark
from .static import Static
from .url import Url
from ..base.type import Path

if t.TYPE_CHECKING:
    from typing_extensions import Self

    from ..base.core import Foam


class Parser:
    '''All parsers'''

    def __init__(self, case: Case, static: Static, url: Url) -> None:
        self.case = case
        self.static = static
        self.url = url

    @classmethod
    def from_foam(cls, foam: 'Foam') -> 'Self':
        return cls(
            Case.default(),
            Static.from_foam(foam),
            Url.from_foam(foam),
        )

    @classmethod
    def to_foam(cls, path: Path, **kwargs: t.Any) -> 'Foam':
        from ..base.core import Foam

        data = Lark.from_path(path, **kwargs).to_foam_data()
        data[0]['version'] = Foam.__version__.to_string()
        return Foam(data, path)
