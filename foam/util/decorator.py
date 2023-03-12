__all__ = ['Match', 'classproperty', 'message', 'suppress']


import contextlib
import functools as f
import io
import typing as t

from ..base.lib import classproperty
from ..base.type import Any, Func1, FuncAny2, Keys, TupleSeq

if t.TYPE_CHECKING:
    import typing_extensions as te

    P = te.ParamSpec('P')


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
        self._methods: t.Dict[TupleSeq[str], FuncAny2] = {}

    def __getitem__(self, keys: Keys[str]) -> FuncAny2:
        if isinstance(keys, tuple):
            return self._methods[keys]
        else:
            return self.__getitem__((keys, ))

    @classmethod
    def default(cls) -> 'te.Self':
        return cls()

    def get(self, *keys: str, default: t.Optional[FuncAny2] = None) -> t.Optional[FuncAny2]:
        return self._methods.get(keys, default)

    def register(self, *types: str) -> Func1[FuncAny2, FuncAny2]:
        '''Register methods for different types'''

        def decorate(func: FuncAny2) -> FuncAny2:
            self._methods[types] = func

            @f.wraps(func)
            def wrapper(*args: 'P.args', **kwargs: 'P.kwargs') -> Any:
                return func(*args, **kwargs)

            return wrapper

        return decorate


class suppress:
    '''Suppress stderr or stdout

    Reference:
        - https://docs.python.org/3/library/unittest.html
        - https://stackoverflow.com/questions/9718950/do-i-have-to-do-stringio-close
    '''

    class _base:
        '''Base'''

        __redirect__: Func1[io.StringIO, Any]

        _previous = ''

        @classmethod
        @contextlib.contextmanager
        def contextWithoutPrevious(cls) -> t.Iterator[io.StringIO]:
            with io.StringIO() as target, cls.__redirect__(target):
                try:
                    yield target
                finally:
                    pass

        @classmethod
        @contextlib.contextmanager
        def contextWithPrevious(cls) -> t.Iterator[io.StringIO]:
            with cls.contextWithoutPrevious() as target:
                try:
                    yield target
                finally:
                    cls._previous = target.getvalue()

        @classmethod
        def decoratorWithoutPrevious(cls, func: FuncAny2) -> FuncAny2:

            @f.wraps(func)
            def wrapper(*args: 'P.args', **kwargs: 'P.kwargs') -> Any:
                with cls.contextWithoutPrevious():
                    return func(*args, **kwargs)

            return wrapper

        @classmethod
        def decoratorWithPrevious(cls, func: FuncAny2) -> FuncAny2:

            @f.wraps(func)
            def wrapper(*args: 'P.args', **kwargs: 'P.kwargs') -> Any:
                with cls.contextWithPrevious():
                    return func(*args, **kwargs)

            return wrapper

        @classproperty
        def previous(cls) -> str:
            return cls._previous

        context_without_previous = contextWithoutPrevious
        context_with_previous = contextWithPrevious
        decorator_without_previous = decoratorWithoutPrevious
        decorator_with_previous = decoratorWithPrevious

        context = contextWithoutPrevious
        decorator = decoratorWithPrevious

    class stderr(_base):
        '''Std Err'''

        __redirect__ = contextlib.redirect_stderr

    class stdout(stderr):
        '''Std Out'''

        __redirect__ = contextlib.redirect_stdout


def message(msg: str = '') -> Func1[FuncAny2, FuncAny2]:

    def decorate(func: FuncAny2) -> FuncAny2:

        @f.wraps(func)
        def wrapper(*args: 'P.args', **kwargs: 'P.kwargs') -> Any:
            print(msg)
            return func(*args, **kwargs)

        return wrapper

    return decorate
