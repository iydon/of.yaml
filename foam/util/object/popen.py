__all__ = ['DryRun', 'Origin']


import subprocess
import typing as t

if t.TYPE_CHECKING:
    import typing_extensions as te


Origin = subprocess.Popen


class DryRun:
    '''Dry run'''

    args = None
    stdout = b''
    returncode = 0

    def __init__(self, *args: t.Any, **kwargs: t.Any) -> None:
        print(f'Popen({self._repr(*args, **kwargs)})')

    def __enter__(self) -> 'te.Self':
        return self

    def __exit__(self, type, value, traceback) -> None:
        pass

    def communicate(self, *args: t.Any, **kwargs: t.Any) -> t.Tuple[bytes, bytes]:
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
