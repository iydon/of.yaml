__all__ = ['Iterator']


import copy
import functools as f
import operator as op
import typing as t

from ..function import deprecated_classmethod
from ...base.type import Ta, Tb, DictAny2, Func1, Func2

if t.TYPE_CHECKING:
    import typing_extensions as te


class Iterator(t.Generic[Ta]):
    '''Iterator (map, filter, reduce)

    Example:
        >>> i1 = Iterator.fromList([-2, -1, 0, 1, 2])
        >>> i2 = i1.filter(bool).map(lambda x: (x, x+1))
        >>> print(i2.copy().collect_as_dict())
        {-2: -1, -1: 0, 1: 2, 2: 3}
        >>> i3 = i2.map(lambda x: x[0]*x[1])
        >>> print(i3.copy().reduce_with_operator('add'))
        10
    '''

    __slots__ = ('_iterator', )

    def __init__(self, iterator: t.Iterator[Ta]) -> None:
        self._iterator = iterator

    def __iter__(self) -> t.Iterator[Ta]:
        return self._iterator

    @classmethod
    def fromDict(cls, iterable: DictAny2) -> 'te.Self[Ta]':
        # Ta = Item = (Key, Value)
        return cls(iter(iterable.items()))

    @classmethod
    def fromIter(cls, iterable: t.Iterable[Ta]) -> 'te.Self[Ta]':
        return cls(iter(iterable))

    @classmethod
    def fromList(cls, iterable: t.List[Ta]) -> 'te.Self[Ta]':
        return cls(iter(iterable))

    def collect(self, func: Func1[t.Iterator[Ta], Tb]) -> Tb:
        return func(self._iterator)

    def collect_as_dict(self) -> DictAny2:
        # Ta = Item = (Key, Value)
        return self.collect(dict)

    def collect_as_list(self) -> t.List[Ta]:
        return self.collect(list)

    def copy(self) -> 'te.Self[Ta]':
        return copy.deepcopy(self)

    def filter(self, func: t.Optional[Func1[Ta, bool]] = None) -> 'te.Self[Ta]':
        return self._new(filter(func, self._iterator))

    def map(self, func: Func1[Ta, Tb]) -> 'te.Self[Tb]':
        return self._new(map(func, self._iterator))

    def reduce(self, func: Func2[Tb, Ta, Tb], initial: t.Optional[Tb] = None) -> Tb:
        if initial is None:
            return f.reduce(func, self._iterator)
        else:
            return f.reduce(func, self._iterator, initial)

    def reduce_with_operator(self, attr: str) -> Ta:
        return self.reduce(getattr(op, attr))

    def _new(self, iterator: t.Iterator[Tb]) -> 'te.Self[Tb]':
        return self.__class__(iterator)

    from_dict = deprecated_classmethod(fromDict)
    from_iter = deprecated_classmethod(fromIter)
    from_list = deprecated_classmethod(fromList)
