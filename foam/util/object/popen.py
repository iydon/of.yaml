__all_ = ['Origin', 'DryRun']


import subprocess
import sys
import typing as t

if t.TYPE_CHECKING:
    from typing_extensions import Self


Origin = subprocess.Popen


class DryRun:
    '''Dry run'''

    args = None
    stdout = b''
    returncode = 0

    def __init__(self, *args: t.Any, **kwargs: t.Any) -> None:
        print(self._repr(*args, **kwargs))
        pass

    def __enter__(self) -> 'Self':
        return self

    def __exit__(self, type, value, traceback) -> None:
        pass

    def communicate(self, *args: t.Any, **kwargs: t.Any) -> None:
        print(self._repr(*args, **kwargs))
        return (b'', b'')

    def poll(self) -> int:
        return self.returncode

    def _repr(self, *args: t.Any, **kwargs: t.Any) -> str:
        func_name = sys._getframe(1).f_code.co_name
        args_repr = ', '.join(repr(arg) for arg in args)
        kwargs_repr = ', '.join(f'{k!s}={v!r}' for k, v in kwargs.items())
        return f'Popen.{func_name}({args_repr}, {kwargs_repr})'
