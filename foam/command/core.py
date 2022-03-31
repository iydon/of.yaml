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
        commands: t.List[str],
        suffix: str = '', overwrite: bool = False, exception: bool = True,
    ) -> t.List[p.Path]:
        '''https://github.com/OpenFOAM/OpenFOAM-7/blob/master/bin/tools/RunFunctions'''
        self._check()
        popen = lambda args: s.Popen(args, cwd=self._foam._dest, stdout=s.PIPE)
        paths = [None] * len(commands)
        for ith, command in enumerate(commands):
            args = shlex.split(command.replace('__app__', self.application))
            path = self._foam._dest / f'log.{args[0]}{suffix}'
            if not overwrite and path.exists():
                message = f'{args[0]} already run on {path.parent.absolute()}: remove log file "{path.name}" to re-run'
                if exception:
                    raise Exception(message)
                else:
                    print(message)
                    continue
            # TODO: rewritten as parenthesized context managers when updated to 3.10
            App = Apps.get(args[0], Default)
            with popen(args) as proc, open(path, 'wb') as file, App(self._foam) as app:
                for line in proc.stdout:
                    file.write(line)
                    app.step(line)
            paths[ith] = path
        return paths

    def raw(self, command: str, output: bool = True) -> s.CompletedProcess:
        '''Execute raw command in case directory'''
        self._check()
        args = shlex.split(command)
        return s.run(args, cwd=self._foam._dest, capture_output=output)

    def _check(self) -> None:
        assert self._foam._dest is not None, 'Please call `Foam::save` method first'
