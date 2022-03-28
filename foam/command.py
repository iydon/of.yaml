__all__ = ['Command']


import subprocess
import time
import typing as t

if t.TYPE_CHECKING:
    from . import Foam


class Command:
    '''OpenFOAM command wrapper'''

    def __init__(self, foam: 'Foam') -> None:
        self._foam = foam

    @property
    def application(self) -> str:
        return self._foam['foam']['system', 'controlDict', 'application']

    def run(self, *command: str, output: bool = True) -> 'Process':
        '''Execute command in case directory'''
        assert self._foam._dest is not None, 'Please call `Foam::save` method first'
        now = time.time()
        cp = subprocess.run(command, cwd=self._foam._dest, capture_output=output)
        return Process(
            code=cp.returncode, time=time.time()-now,
            stdout=cp.stdout, stderr=cp.stderr,
        )


class Process(t.NamedTuple):
    code: int
    time: float
    stdout: t.Optional[bytes] = None
    stderr: t.Optional[bytes] = None
