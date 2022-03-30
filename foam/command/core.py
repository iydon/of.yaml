__all__ = ['Command']


import pathlib as p
import shlex
import subprocess as s
import typing as t

from .progress import Default, Apps

if t.TYPE_CHECKING:
    from ..core import Foam


class Command:
    '''OpenFOAM command wrapper'''

    def __init__(self, foam: 'Foam') -> None:
        self._foam = foam

    @property
    def application(self) -> str:
        return self._foam['foam']['system', 'controlDict', 'application']

    def run(
        self,
        *commands: str,
        suffix: str = '', overwrite: bool = False,
    ) -> t.List[p.Path]:
        '''https://github.com/OpenFOAM/OpenFOAM-7/blob/master/bin/tools/RunFunctions'''
        import tqdm

        paths = [None] * len(commands)
        for ith, command in enumerate(commands):
            command = shlex.split(command or self.application)
            path = self._foam._dest / f'log.{command[0]}{suffix}'
            if not overwrite and path.exists():
                raise Exception(
                    f'{command[0]} already run on {path.parent.absolute()}: '
                    f'remove log file "{path.name}" to re-run'
                )
            process = s.Popen(command, cwd=self._foam._dest, stdout=s.PIPE)
            start = self._foam['foam']['system', 'controlDict', 'startTime']
            end = self._foam['foam']['system', 'controlDict', 'endTime']
            app = Apps.get(command[0], Default)(start, end)
            with open(path, 'wb') as f:
                with tqdm.tqdm(total=float(end)-float(start)) as pbar:
                    for line in process.stdout:
                        f.write(line)
                        pbar.update(app.delta(line))
            paths[ith] = path
        return paths

    def exec(self, command: str, output: bool = True) -> s.CompletedProcess:
        '''Execute raw command in case directory'''
        assert self._foam._dest is not None, 'Please call `Foam::save` method first'
        args = shlex.split(command)
        return s.run(args, cwd=self._foam._dest, capture_output=output)
