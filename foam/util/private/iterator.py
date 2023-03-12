__all__ = ['Iterator']


import copy
import functools as f
import operator as op
import typing as t

from ..function import deprecated_classmethod
from ...base.type import Any, DictAny2, Func1, Func2, ListAny

if t.TYPE_CHECKING:
    import typing_extensions as te


class Iterator:
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

    def __init__(self, iterator: t.Iterator[Any]) -> None:
        self._iterator = iterator

    def __iter__(self) -> t.Iterator[Any]:
        return self._iterator

    @classmethod
    def fromDict(cls, iterable: DictAny2) -> 'te.Self':
        return cls(iter(iterable.items()))

    @classmethod
    def fromIter(cls, iterable: t.Iterable[Any]) -> 'te.Self':
        return cls(iter(iterable))

    @classmethod
    def fromList(cls, iterable: ListAny) -> 'te.Self':
        return cls(iter(iterable))

    def collect(self, func: Func1[t.Iterator[Any], Any]) -> Any:
        return func(self._iterator)

    def collect_as_dict(self) -> DictAny2:
        return self.collect(dict)

    def collect_as_list(self) -> ListAny:
        return self.collect(list)

    def copy(self) -> 'te.Self':
        return copy.deepcopy(self)

    def filter(self, func: t.Optional[Func1[Any, Any]] = None) -> 'te.Self':
        return self._new(filter(func, self._iterator))

    def map(self, func: Func1[Any, Any]) -> 'te.Self':
        return self._new(map(func, self._iterator))

    def reduce(self, func: Func2[Any, Any, Any]) -> Any:
        return f.reduce(func, self._iterator)

    def reduce_with_operator(self, attr: str) -> Any:
        return self.reduce(getattr(op, attr))

    def _new(self, iterator: t.Iterator[Any]) -> 'te.Self':
        return self.__class__(iterator)

    from_dict = deprecated_classmethod(fromDict)
    from_iter = deprecated_classmethod(fromIter)
    from_list = deprecated_classmethod(fromList)
