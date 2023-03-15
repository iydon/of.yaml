__all__ = ['Parser']


import typing as t

from .case import Case
from .lark import Lark
from .static import Static
from .url import Url
from ..base.type import Path
from ..util.function import deprecated_classmethod
from ..util.implementation import Base

if t.TYPE_CHECKING:
    import typing_extensions as te

    from ..base.core import Foam

    P = te.ParamSpec('P')
    Kwargs = te.ParamSpecKwargs(P)


class Parser(Base):
    '''All parsers'''

    __slots__ = ('case', 'static', 'url')

    def __init__(self, case: Case, static: Static, url: Url) -> None:
        self.case = case
        self.static = static
        self.url = url

    @classmethod
    def default(cls) -> 'te.Self':
        from ..base.core import Foam

        return cls.fromFoam(Foam.default())

    @classmethod
    def fromFoam(cls, foam: 'Foam') -> 'te.Self':
        return cls(
            Case.default(),
            Static.fromFoam(foam),
            Url.fromFoam(foam),
        )

    @classmethod
    def toFoam(cls, path: Path, **kwargs: 'Kwargs') -> 'Foam':
        from ..base.core import Foam

        data = Lark.fromPath(path, **kwargs).to_foam_data()
        data[0]['version'] = Foam.__version__.to_string()
        return Foam(data, path)

    from_foam = deprecated_classmethod(fromFoam)
    to_foam = deprecated_classmethod(toFoam)
