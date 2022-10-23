__all__ = ['classproperty', 'Match']


import functools as f
import typing as t

from ..base.lib import classproperty
from ..base.type import Keys

if t.TYPE_CHECKING:
    from typing_extensions import Self


class Match:
    '''Use decorator to simulate match syntax

    Example:
        >>> match = Match.default()

        >>> @match.register()
        ... def _():
        ...     return 0

        >>> @match.register('x')
        ... def _():
        ...     return 1

        >>> @match.register('x', 'y')
        ... def _():
        ...     return 2

        >>> match[()]()
        0
        >>> match['x']()
        1
        >>> match['x', 'y']()
        2
    '''

    def __init__(self) -> None:
        self._methods: t.Dict[t.Tuple[str, ...], t.Callable] = {}

    def __getitem__(self, keys: Keys[str]) -> t.Callable:
        if not isinstance(keys, tuple):
            return self.__getitem__((keys, ))
        return self._methods[keys]

    @classmethod
    def default(cls) -> 'Self':
        return cls()

    def get(self, *keys: str, default: t.Optional[t.Callable] = None) -> t.Optional[t.Callable]:
        return self._methods.get(keys, default)

    def register(self, *types: str) -> t.Callable:
        '''Register methods for different types'''

        def decorate(func: t.Callable) -> t.Callable:
            self._methods[types] = func

            @f.wraps(func)
            def wrapper(*args: t.Any, **kwargs: t.Any) -> t.Any:
                return func(*args, **kwargs)

            return wrapper

        return decorate
