__all__ = ['DryRun', 'Origin']


import subprocess
import typing as t

from ...base.type import Any

if t.TYPE_CHECKING:
    import typing_extensions as te

    P = te.ParamSpec('P')
    Args, Kwargs = te.ParamSpecArgs(P), te.ParamSpecKwargs(P)


Origin = subprocess.Popen


class DryRun:
    '''Dry run'''

    __slots__ = ()
    args = None
    stdout = b''
    returncode = 0

    def __init__(self, *args: 'P.args', **kwargs: 'P.kwargs') -> None:
        print(f'Popen({self._repr(*args, **kwargs)})')

    def __enter__(self) -> 'te.Self':
        return self

    def __exit__(self, type: Any, value: Any, traceback: Any) -> None:
        pass

    def communicate(self, *args: 'P.args', **kwargs: 'P.kwargs') -> t.Tuple[bytes, bytes]:
        print(f'Popen.communicate({self._repr(*args, **kwargs)})')
        return (b'', b'')

    def poll(self) -> int:
        return self.returncode

    def _repr(self, *args: 'P.args', **kwargs: 'P.kwargs') -> str:
        # caller_func_name = sys._getframe(1).f_code.co_name
        return f'{self._repr_args(*args)}, {self._repr_kwargs(**kwargs)}'

    def _repr_args(self, *args: 'Args') -> str:
        return ', '.join(repr(arg) for arg in args)

    def _repr_kwargs(self, **kwargs: 'Kwargs') -> str:
        return ', '.join(f'{k!s}={v!r}' for k, v in kwargs.items())
