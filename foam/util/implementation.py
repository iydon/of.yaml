__all__ = ['Singleton']


import typing as t

from ..base.type import DictStr
from ..compat.typing import Protocol

if t.TYPE_CHECKING:
    import typing_extensions as te

    P = te.ParamSpec('P')


class Singleton(Protocol):
    '''Singleton'''

    # __slots__ = ...  # __dict__ slot disallowed: we already got one
    __instances: DictStr['te.Self'] = {}

    @classmethod
    def default(cls) -> 'te.Self':
        return cls.new()

    @classmethod
    def new(cls, *args: 'P.args', **kwargs: 'P.kwargs') -> 'te.Self':
        key = cls.__hash(*args, **kwargs)
        if key not in cls.__instances:
            cls.__instances[key] = cls(*args, **kwargs)
        return cls.__instances[key]

    @classmethod
    def __hash(cls, *args: 'P.args', **kwargs: 'P.kwargs') -> str:
        return repr(args) + repr(kwargs)
