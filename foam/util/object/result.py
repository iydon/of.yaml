__all__ = ['Result']


import typing as t

from ...base.type import Ta, Tb, Tc, Func1

if t.TYPE_CHECKING:
    import typing_extensions as te

    from .option import Option


class Result(t.Generic[Ta, Tb]):
    '''
    Example:
        >>> try:
        ...     1 / 0
        ... except Exception as e:
        ...     x = Result.err(e)
        >>> y, z = x.get_ok(), x.get_err()
        >>> print(x, y, z, sep=', ')
        Err(ZeroDivisionError('division by zero')), None, Some(ZeroDivisionError('division by zero'))

    Reference:
        - https://doc.rust-lang.org/std/result/
        - https://doc.rust-lang.org/src/core/result.rs.html
    '''

    __slots__ = ('_ok', '_err')

    def __init__(self, ok: t.Optional[Ta] = None, err: t.Optional[Tb] = None) -> None:
        self._ok = ok
        self._err = err

    def __repr__(self) -> str:
        return self._match(lambda o: f'Result::Ok({o!r})', lambda e: f'Result::Err({e!r})')

    @classmethod
    def default(cls) -> 'te.Self[Ta, Tb]':
        raise NotImplementedError

    @classmethod
    def new(cls, ok: t.Optional[Ta] = None, err: t.Optional[Tb] = None) -> 'te.Self[Ta, Tb]':
        assert (ok is None and err is not None) or (ok is not None and err is None)

        return cls(ok, err)

    @classmethod
    def ok(cls, ok: Ta) -> 'te.Self[Ta, Tb]':
        return cls(ok, None)

    @classmethod
    def err(cls, err: Tb) -> 'te.Self[Ta, Tb]':
        return cls(None, err)

    def is_ok(self) -> bool:
        return self._ok is not None

    def is_ok_and(self, f: Func1[Ta, bool]) -> bool:
        return self.is_ok() and f(self._ok)

    def is_err(self) -> bool:
        return not self.is_ok()

    def is_err_and(self, f: Func1[Tb, bool]) -> bool:
        return self.is_err() and f(self._err)

    def get_ok(self) -> 'Option[Ta]':
        # https://doc.rust-lang.org/src/core/result.rs.html#642
        from .option import Option

        return Option.new(self._ok)

    def get_err(self) -> 'Option[Tb]':
        # https://doc.rust-lang.org/src/core/result.rs.html#673
        from .option import Option

        return Option.new(self._err)

    def map(self, f: Func1[Ta, Tc]) -> 'te.Self[Tc, Tb]':
        return self._match(lambda o: self.ok(f(o)), lambda e: self)

    def map_or(self, default: Tc, f: Func1[Ta, Tc]) -> Tc:
        return self._match(lambda o: f(o), lambda e: default)

    def map_or_else(self, default: Func1[Tb, Tc], f: Func1[Ta, Tc]) -> Tc:
        return self._match(lambda o: f(o), lambda e: default(e))

    def map_err(self, f: Func1[Tb, Tc]) -> 'te.Self[Ta, Tc]':
        return self._match(lambda o: self, lambda e: self.err(f(e)))

    def inspect(self, f: Func1[Ta, None]) -> 'te.Self[Ta, Tb]':
        if self.is_ok():
            f(self._ok)
        return self

    def inspect_err(self, f: Func1[Tb, None]) -> 'te.Self[Ta, Tb]':
        if self.is_err():
            f(self._err)
        return self

    def expect(self, msg: str) -> Ta:
        assert self.is_ok(), msg

        return self._ok

    def unwrap(self) -> Ta:
        return self.expect('called `Result::unwrap()` on an `Err` value')

    def unwrap_or_default(self) -> Ta:
        # https://doc.rust-lang.org/src/core/result.rs.html#1143
        raise NotImplementedError

    def expect_err(self, msg: str) -> Tb:
        assert self.is_err(), msg

        return self._err

    def unwrap_err(self) -> Tb:
        return self.expect_err('called `Result::unwrap_err()` on an `Ok` value')

    def into_ok(self) -> Ta:
        # https://doc.rust-lang.org/src/core/result.rs.html#1240
        raise NotImplementedError

    def into_ok(self) -> Tb:
        # https://doc.rust-lang.org/src/core/result.rs.html#1277
        raise NotImplementedError

    def and_(self, res: 'te.Self[Tc, Tb]') -> 'te.Self[Tc, Tb]':
        return self._match(lambda o: res, lambda e: self)

    def and_then(self, op: Func1[Ta, 'te.Self[Tc, Tb]']) -> 'te.Self[Tc, Tb]':
        return self._match(lambda o: op(o), lambda: self)

    def or_(self, res: 'te.Self[Ta, Tc]') -> 'te.Self[Ta, Tc]':
        return self._match(lambda o: self, lambda e: res)

    def or_else(self, op: Func1[Tb, 'te.Self[Ta, Tc]']) -> 'te.Self[Ta, Tc]':
        return self._match(lambda o: self, lambda e: op(e))

    def unwrap_or(self, default: Ta) -> Ta:
        return self._match(lambda o: o, lambda e: default)

    def unwrap_or_else(self, op: Func1[Tb, Ta]) -> Ta:
        return self._match(lambda o: o, lambda e: op(e))

    def contains(self, x: Ta) -> bool:
        return self._match(lambda o: o==x, lambda e: False)

    def contains_err(self, f: Tb) -> bool:
        return self._match(lambda o: False, lambda e: e==f)

    def _match(self, f4ok: Func1[Ta, Tc], f4err: Func1[Tb, Tc]) -> Tc:
        if self.is_ok():
            return f4ok(self._ok)
        else:
            return f4err(self._err)
