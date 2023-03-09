__all__ = ['Singleton']


import typing as t

from ..compat.typing import Protocol

if t.TYPE_CHECKING:
    import typing_extensions as te


class Singleton(Protocol):
    '''Singleton'''

    __instances = {}

    @classmethod
    def default(cls) -> 'te.Self':
        return cls.new()

    @classmethod
    def new(cls, *args: t.Any, **kwargs: t.Any) -> 'te.Self':
        key = cls.__hash(*args, **kwargs)
        if key not in cls.__instances:
            cls.__instances[key] = cls(*args, **kwargs)
        return cls.__instances[key]

    @classmethod
    def __hash(cls, *args: t.Any, **kwargs: t.Any) -> str:
        return repr(args) + repr(kwargs)
