__all__ = ['Singleton']


import typing as t

from ..compat.typing import Protocol

if t.TYPE_CHECKING:
    from typing_extensions import Self


class Singleton(Protocol):
    '''Singleton'''

    _instances = {}

    @classmethod
    def default(cls) -> 'Self':
        return cls.new()

    @classmethod
    def new(cls, *args: t.Any, **kwargs: t.Any) -> 'Self':
        key = cls._hash(*args, **kwargs)
        if key not in cls._instances:
            cls._instances[key] = cls(*args, **kwargs)
        return cls._instances[key]

    @classmethod
    def _hash(cls, *args: t.Any, **kwargs: t.Any) -> str:
        return repr(args) + repr(kwargs)
