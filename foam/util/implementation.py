__all__ = ['Base', 'Singleton']


import typing as t

from ..compat.typing import Protocol

if t.TYPE_CHECKING:
    import typing_extensions as te

    P = te.ParamSpec('P')


class Base(Protocol):
    '''Base classmethod protocol'''

    # __slots__ = ...  # __dict__ slot disallowed: we already got one

    @classmethod
    def default(cls) -> 'te.Self':
        raise NotImplementedError

    @classmethod
    def new(cls, *args: 'P.args', **kwargs: 'P.kwargs') -> 'te.Self':
        return cls(*args, **kwargs)


class Singleton(Protocol):
    '''Singleton protocol'''

    # __slots__ = ...  # __dict__ slot disallowed: we already got one
    __instance: t.Dict[t.Tuple[int, int], 'te.Self'] = {}

    @classmethod
    def default(cls) -> 'te.Self':
        raise NotImplementedError

    @classmethod
    def new(cls, *args: 'P.args', **kwargs: 'P.kwargs') -> 'te.Self':
        key = (hash(args), hash(frozenset(kwargs.items())))
        if key not in cls.__instance:
            cls.__instance[key] = cls(*args, **kwargs)
        return cls.__instance[key]
