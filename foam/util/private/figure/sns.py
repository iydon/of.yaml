__all__ = ['AddOn']


import typing as t

from ...implementation import Base
from ....base.type import Any, FuncAny

if t.TYPE_CHECKING:
    import typing_extensions as te

    from . import Figure

    P = te.ParamSpec('P')


Wrapper = FuncAny['Figure']


class AddOn(Base):
    '''seaborn

    TODO:
        - everything
    '''

    __slots__ = ('_figure', '_ret')

    def __init__(self, figure: 'Figure') -> None:
        self._figure = figure
        self._ret = None

    @property
    def ret(self) -> Any:
        return self._ret

    def _wrapper(self, name: str, /, *args: 'P.args', **kwargs: 'P.kwargs') -> 'Figure':
        self._ret = getattr(self._figure._ax, name)(*args, **kwargs)
        return self._figure
