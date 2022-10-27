__all__ = ['classproperty', 'Match', 'suppress']


import contextlib
import functools as f
import io
import typing as t

from ..base.lib import classproperty
from ..base.type import Keys, TupleSequence

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
        self._methods: t.Dict[TupleSequence[str], t.Callable] = {}

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


class suppress:
    '''Suppress stderr or stdout

    Reference:
        - https://docs.python.org/3/library/unittest.html
        - https://stackoverflow.com/questions/9718950/do-i-have-to-do-stringio-close
    '''

    _stderr_previous = ''
    _stdout_previous = ''

    @classmethod
    def stderr(cls, func: t.Callable) -> t.Callable:

        @f.wraps(func)
        def wrapper(*args: t.Any, **kwargs: t.Any) -> t.Any:
            with io.StringIO() as target:
                with contextlib.redirect_stderr(target):
                    ans = func(*args, **kwargs)
                cls.stderr_previous = target.getvalue()
            return ans

        return wrapper

    @classmethod
    def stdout(cls, func: t.Callable) -> t.Callable:

        @f.wraps(func)
        def wrapper(*args: t.Any, **kwargs: t.Any) -> t.Any:
            with io.StringIO() as target:
                with contextlib.redirect_stdout(target):
                    ans = func(*args, **kwargs)
                cls.stdout_previous = target.getvalue()
            return ans

        return wrapper

    @classproperty
    def stderr_previous(cls) -> str:
        return cls._stderr_previous

    @classproperty
    def stdout_previous(cls) -> str:
        return cls._stdout_previous
