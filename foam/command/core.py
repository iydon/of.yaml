__all__ = ['Command']


import functools as f
import pathlib as p
import shlex
import subprocess as s
import typing as t
import warnings as w

from .progress import Default, Apps

if t.TYPE_CHECKING:
    from ..core import Foam


class Command:
    '''OpenFOAM command wrapper'''

    Self = __qualname__

    def __init__(self, foam: 'Foam') -> None:
        self._foam = foam

    @classmethod
    def from_foam(cls, foam: 'Foam') -> Self:
        return cls(foam)

    @property
    def times(self) -> t.List[float]:
        times = []
        for path in self._foam._dest.iterdir():
            try:
                time = float(path.stem)
            except ValueError:
                continue
            times.append(time)
        return sorted(times)

    @f.cached_property
    def macros(self) -> t.Dict[str, str]:
        return {
            '__app__': self._foam.application,
            '__procs__': str(self._foam.number_of_processors),
            '__pwd__': self._foam._dest.absolute().as_posix(),
        }

    def all_run(
        self,
        overwrite: bool = False, exception: bool = False,
        parallel: bool = True, unsafe: bool = True,
    ) -> None:
        if not self._foam.pipeline:
            assert (self._foam._dest/'Allrun').exists()
            self.raw('./Allrun')
        else:
            self.run(self._foam.pipeline, overwrite=overwrite, exception=exception, parallel=parallel, unsafe=unsafe)

    def all_clean(self) -> None:
        # TODO: https://github.com/OpenFOAM/OpenFOAM-7/blob/master/bin/tools/CleanFunctions
        self.raw('./Allclean')

    def run(
        self,
        commands: t.List[str],
        suffix: str = '', overwrite: bool = False, exception: bool = True,
        parallel: bool = True, unsafe: bool = False,
    ) -> t.List[p.Path]:
        '''https://github.com/OpenFOAM/OpenFOAM-7/blob/master/bin/tools/RunFunctions'''
        popen = lambda args: s.Popen(
            ' '.join(args) if unsafe else args,
            cwd=self._foam._dest, shell=unsafe, stdout=s.PIPE,
        )
        paths = [None] * len(commands)
        for ith, command in enumerate(commands):
            raws = shlex.split(self._replace(command))
            args = self._split(command, parallel and self._foam.number_of_processors>1)
            path = self._foam._dest / f'log.{raws[0].replace("./", "")}{suffix}'
            if not overwrite and path.exists():
                message = f'{raws[0]} already run on {path.parent.absolute()}: remove log file "{path.name}" to re-run'
                if exception:
                    raise Exception(message)
                else:
                    w.warn(message)
                    continue
            print(f'Running {raws[0]} on {path.parent.absolute()} using {self._foam.number_of_processors} processes if in parallel')
            # TODO: rewritten as parenthesized context managers when updated to 3.10
            App = Apps.get(raws[0], Default)
            with popen(args) as proc, open(path, 'wb') as file, App(self._foam) as app:
                for line in proc.stdout:
                    file.write(line)
                    app.step(line)
            paths[ith] = path
        # TODO: use exit status as return
        return paths

    def raw(self, command: str, output: bool = True) -> s.CompletedProcess:
        '''Execute raw command in case directory'''
        args = shlex.split(command)
        return s.run(args, cwd=self._foam._dest, capture_output=output)

    def _replace(self, command: str) -> str:
        for old, new in self.macros.items():
            command = command.replace(old, new)
        return command

    def _split(self, command: str, parallel: bool) -> t.List[str]:
        if parallel and '__app__' in command:
            command = f'mpirun -np __procs__ {command} -parallel'
        return shlex.split(self._replace(command))
