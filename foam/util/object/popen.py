__all_ = ['Origin', 'DryRun']


import subprocess
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
        print(f'Popen({self._repr(*args, **kwargs)})')

    def __enter__(self) -> 'Self':
        return self

    def __exit__(self, type, value, traceback) -> None:
        pass

    def communicate(self, *args: t.Any, **kwargs: t.Any) -> None:
        print(f'Popen.communicate({self._repr(*args, **kwargs)})')
        return (b'', b'')

    def poll(self) -> int:
        return self.returncode

    def _repr(self, *args: t.Any, **kwargs: t.Any) -> str:
        # caller_func_name = sys._getframe(1).f_code.co_name
        return f'{self._repr_args(*args)}, {self._repr_kwargs(**kwargs)}'

    def _repr_args(self, *args: t.Any) -> str:
        return ', '.join(repr(arg) for arg in args)

    def _repr_kwargs(self, **kwargs: t.Any) -> str:
        return ', '.join(f'{k!s}={v!r}' for k, v in kwargs.items())
