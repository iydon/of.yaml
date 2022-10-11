__all__ = ['Parser']


import typing as t

from .static import Static
from .url import Url
from .yaml import YAML

if t.TYPE_CHECKING:
    from typing_extensions import Self

    from ..base.core import Foam


class Parser:
    '''All parsers'''

    def __init__(self, static: Static, url: Url, yaml: YAML) -> None:
        self.static = static
        self.url = url
        self.yaml = yaml

    @classmethod
    def from_foam(cls, foam: 'Foam') -> 'Self':
        return cls(
            Static.from_foam(foam),
            Url.from_foam(foam),
            YAML.default(),
        )
