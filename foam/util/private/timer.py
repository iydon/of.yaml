__all__ = ['Timer', 'TimerResult']


import contextlib
import time
import typing as t
import warnings as w

from ...base.type import Any, DictStrFloat, Func0, Func1, Keys
from ...compat.functools import cached_property

if t.TYPE_CHECKING:
    import typing_extensions as te


class Timer:
    '''Timer

    Example:
        >>> timer = Timer.default()
        >>> with timer.tic_toc('1', '2', '3') as t:
        ...     time.sleep(9)
        >>> print(float(t), timer['1', '2', '3'])
        9.00686868999037 9.00686868999037

    Reference:
        - https://docs.python.org/3/library/time.html
        - https://stackoverflow.com/questions/5849800/what-is-the-python-equivalent-of-matlabs-tic-and-toc-functions
    '''

    __slots__ = ('_func', '_cache', '__dict__')

    def __init__(self, func: Func0[float]) -> None:
        self._func = func
        self._cache = {}

    def __enter__(self) -> 'te.Self':
        return self

    def __exit__(self, type: Any, value: Any, traceback: Any) -> None:
        pass

    def __getitem__(self, labels: Keys[t.Hashable]) -> float:
        if not isinstance(labels, tuple):
            return self.__getitem__((labels, ))
        return -self._cache[labels]

    def __repr__(self) -> str:
        return f'Timer.{self._func.__name__}()'

    def __str__(self) -> str:
        return f'<Timer @ time.{self._func.__name__}>'

    @classmethod
    def best(cls) -> 'te.Self':
        names = {'monotonic', 'perf_counter', 'process_time', 'thread_time', 'time'}
        order: Func1['time._ClockInfo', t.Tuple[float, bool, bool]] \
            = lambda info: (info.resolution, not info.monotonic, info.adjustable)
        key: Func1[str, t.Tuple[float, bool, bool]] \
            = lambda name: order(time.get_clock_info(name))
        return getattr(cls, min(names, key=key))()

    @classmethod
    def default(cls) -> 'te.Self':
        return cls.perf_counter()

    @classmethod
    def monotonic(cls) -> 'te.Self':
        '''Return the value (in fractional seconds) of a monotonic clock, i.e. a clock that cannot go backwards. The clock is not affected by system clock updates. The reference point of the returned value is undefined, so that only the difference between the results of two calls is valid.'''
        return cls(time.monotonic)

    @classmethod
    def perfCounter(cls) -> 'te.Self':
        '''Return the value (in fractional seconds) of a performance counter, i.e. a clock with the highest available resolution to measure a short duration. It does include time elapsed during sleep and is system-wide. The reference point of the returned value is undefined, so that only the difference between the results of two calls is valid.'''
        return cls(time.perf_counter)

    @classmethod
    def processTime(cls) -> 'te.Self':
        '''Return the value (in fractional seconds) of the sum of the system and user CPU time of the current process. It does not include time elapsed during sleep. It is process-wide by definition. The reference point of the returned value is undefined, so that only the difference between the results of two calls is valid.'''
        return cls(time.process_time)

    @classmethod
    def threadTime(cls) -> 'te.Self':
        '''Return the value (in fractional seconds) of the sum of the system and user CPU time of the current thread. It does not include time elapsed during sleep. It is thread-specific by definition. The reference point of the returned value is undefined, so that only the difference between the results of two calls in the same thread is valid.'''
        return cls(time.thread_time)

    @classmethod
    def time(cls) -> 'te.Self':
        '''
        Return the time in seconds since the epoch as a floating point number. The specific date of the epoch and the handling of leap seconds is platform dependent. On Windows and most Unix systems, the epoch is January 1, 1970, 00:00:00 (UTC) and leap seconds are not counted towards the time in seconds since the epoch. This is commonly referred to as Unix time. To find out what the epoch is on a given platform, look at gmtime(0).

        Note that even though the time is always returned as a floating point number, not all systems provide time with a better precision than 1 second. While this function normally returns non-decreasing values, it can return a lower value than a previous call if the system clock has been set back between the two calls.

        The number returned by time() may be converted into a more common time format (i.e. year, month, day, hour, etc…) in UTC by passing it to gmtime() function or in local time by passing it to the localtime() function. In both cases a struct_time object is returned, from which the components of the calendar date may be accessed as attributes.
        '''
        return cls(time.time)

    @property
    def cache(self) -> DictStrFloat:
        return self._cache

    @contextlib.contextmanager
    def tic_toc(self, *labels: t.Hashable, builtin: bool = False) -> t.Iterator['TimerResult']:
        if labels in self._cache:
            w.warn(f'Label {labels} already exists')
        try:
            self._cache[labels] = self._func()
            yield self._result(*labels) if builtin else TimerResult(self, *labels)
        finally:
            self._cache[labels] -= self._func()

    def reset(self) -> 'te.Self':
        self._cache.clear()
        return self

    def wait(self, seconds: float) -> 'te.Self':
        time.sleep(seconds)
        return self

    @cached_property
    def _result(self) -> type:
        return type('TimerResult', (), {
            '__slots__': ('_labels', ),
            '__init__': lambda this, *labels: setattr(this, '_labels', labels),
            '__float__': lambda this: self.__getitem__(this._labels),
            '__repr__': lambda this: f'TimerResult({self!r}, {", ".join(map(repr, this._labels))})',
            '__str__': lambda this: f'<TimerResult @ ({", ".join(map(repr, this._labels))})>',
            'value': property(lambda this: this.__float__()),
        })

    perf_counter = perfCounter
    process_time = processTime
    thread_time = threadTime


class TimerResult:
    '''Result for timer'''

    __slots__ = ('_timer', '_labels')

    def __init__(self, timer: 'Timer', *labels: str) -> None:
        self._timer = timer
        self._labels = labels

    def __float__(self) -> float:
        return self._timer.__getitem__(self._labels)

    def __repr__(self) -> str:
        return f'TimerResult({self._timer!r}, {", ".join(map(repr, self._labels))})'

    def __str__(self) -> str:
        return f'<TimerResult @ ({", ".join(map(repr, self._labels))})>'

    @property
    def value(self) -> float:
        return self.__float__()
