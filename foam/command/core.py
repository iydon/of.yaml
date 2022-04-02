__all__ = ['Command']


import functools as f
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

    @f.cached_property
    def macros(self) -> t.Dict[str, str]:
        return {
            '__app__': self.application,
            '__procs__': str(self.number_of_processors),
        }

    @f.cached_property
    def application(self) -> str:
        return self._foam['foam']['system', 'controlDict', 'application']

    @f.cached_property
    def number_of_processors(self) -> int:
        try:
            return self._foam['foam']['system', 'decomposeParDict', 'numberOfSubdomains']
        except:
            return 1

    def all_run(self) -> None:
        pipe = (self._foam['other'] or {}).get('pipeline', None)
        if pipe is None:
            self.raw('./Allrun')
        else:
            self.run(pipe, overwrite=False, exception=False, parallel=True, unsafe=True)

    def run(
        self,
        commands: t.List[str],
        suffix: str = '', overwrite: bool = False, exception: bool = True,
        parallel: bool = True, unsafe: bool = False,
    ) -> t.List[p.Path]:
        '''https://github.com/OpenFOAM/OpenFOAM-7/blob/master/bin/tools/RunFunctions'''
        self._check()
        popen = lambda args: s.Popen(
            ' '.join(args) if unsafe else args,
            cwd=self._foam._dest, shell=unsafe, stdout=s.PIPE,
        )
        paths = [None] * len(commands)
        for ith, command in enumerate(commands):
            raws = shlex.split(self._replace(command))
            args = self._split(command, parallel and self.number_of_processors>1)
            path = self._foam._dest / f'log.{raws[0].replace("./", "")}{suffix}'
            if not overwrite and path.exists():
                message = f'{raws[0]} already run on {path.parent.absolute()}: remove log file "{path.name}" to re-run'
                if exception:
                    raise Exception(message)
                else:
                    print(message)
                    continue
            print(f'Running {raws[0]} on {path.parent.absolute()}')
            # TODO: rewritten as parenthesized context managers when updated to 3.10
            App = Apps.get(raws[0], Default)
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

    def _replace(self, command: str) -> str:
        for old, new in self.macros.items():
            command = command.replace(old, new)
        return command

    def _split(self, command: str, parallel: bool) -> t.List[str]:
        if parallel and '__app__' in command:
            command = f'mpirun -np __procs__ {command} -parallel'
        return shlex.split(self._replace(command))
