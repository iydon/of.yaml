__all__ = ['Command']


import functools as f
import pathlib as p
import shlex
import shutil
import subprocess as s
import typing as t
import warnings as w

from .adapter import Default, Apps
from ...base.type import Dict

if t.TYPE_CHECKING:
    from typing_extensions import Self

    from ...base.core import Foam


class Command:
    '''OpenFOAM command wrapper'''

    def __init__(self, foam: 'Foam') -> None:
        self._foam = foam

    @classmethod
    def from_foam(cls, foam: 'Foam') -> 'Self':
        foam.destination  # assert dest is not None
        return cls.from_foam_without_asserting(foam)

    @classmethod
    def from_foam_without_asserting(cls, foam: 'Foam') -> 'Self':
        return cls(foam)

    @property
    def times(self) -> t.List[float]:
        '''Time directories'''
        times = []
        for path in self._foam.destination.iterdir():
            try:
                time = float(path.name)
            except ValueError:
                continue
            times.append(time)
        return sorted(times)

    @property
    def logs(self) -> t.Set[p.Path]:
        '''Log files'''
        logs = set()
        for path in self._foam.destination.iterdir():
            if path.stem == 'log':
                logs.add(path)
        return logs

    @f.cached_property
    def macros(self) -> t.Dict[str, str]:
        '''Macros that can be used in the pipeline field'''
        macros = {
            '__app__': self._foam.application,
            '__procs__': str(self._foam.number_of_processors),
        }
        try:
            macros['__pwd__'] = self._foam.destination.absolute().as_posix()
        except AssertionError:
            pass
        return macros

    def all_run(
        self,
        overwrite: bool = False, exception: bool = False,
        parallel: bool = True, unsafe: bool = True,
    ) -> t.List[int]:
        '''Inspired by  `Allrun`'''
        if not self._foam.pipeline:
            assert (self._foam.destination/'Allrun').exists()

            return [self.raw('./Allrun').returncode]
        else:
            return self.run(self._foam.pipeline, overwrite=overwrite, exception=exception, parallel=parallel, unsafe=unsafe)

    def all_clean(self) -> None:
        '''Inspired by `Allclean`'''
        # TODO: https://github.com/OpenFOAM/OpenFOAM-7/blob/master/bin/tools/CleanFunctions
        shutil.rmtree(self._foam.destination)
        self._foam.save(self._foam.destination)

    def run(
        self,
        commands: t.List[t.Union[str, Dict]],
        suffix: str = '', overwrite: bool = False, exception: bool = True,
        parallel: bool = True, unsafe: bool = False,
    ) -> t.List[int]:
        '''Inspired by `runApplication` and `runParallel`

        - Reference:
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/bin/tools/RunFunctions
        '''
        codes: t.List[int] = [-1] * len(commands)
        for ith, command in enumerate(commands):
            option = self._command(command, suffix=suffix, overwrite=overwrite, exception=exception, parallel=parallel)
            raws = self._split(option['command'], False)
            args = self._split(option['command'], option['parallel'] and self._foam.number_of_processors>1)
            path = self._foam.destination / f'log.{raws[0].replace("./", "")}{option["suffix"]}'
            # Option: overwrite, exception
            if not option['overwrite'] and path.exists():
                message = f'{raws[0]} already run on {path.parent.absolute()}: remove log file "{path.name}" to re-run'
                if option['exception']:
                    raise Exception(message)
                else:
                    w.warn(message)
                    continue
            # TODO: verbose?
            print(f'Running {raws[0]} on {path.parent.absolute()} using {self._foam.number_of_processors} processes if in parallel')
            # TODO: rewritten as parenthesized context managers when updated to 3.10
            App = Apps.get(raws[0], Default)
            with self._popen(args, unsafe) as proc, open(path, 'wb') as file, App(self._foam) as app:
                for line in proc.stdout:
                    file.write(line)
                    app.step(line)
            codes[ith] = proc.returncode
        return codes

    def raw(self, command: str, output: bool = True) -> s.CompletedProcess:
        '''Execute raw command in case directory'''
        args = shlex.split(command)
        return s.run(args, cwd=self._foam._dest, capture_output=output)  # Deliberate use of the _dest

    def which(self, command: str) -> t.Optional[str]:
        stdout = self.raw(f'which {command}', output=True).stdout.decode().strip()
        return stdout or None

    def _replace(self, command: str) -> str:
        for old, new in self.macros.items():
            command = command.replace(old, new)
        return command

    def _split(self, command: str, parallel: bool, replace: bool = True) -> t.List[str]:
        if parallel and '__app__' in command:
            command = f'mpirun -np __procs__ {command} -parallel'
        if replace:
            command = self._replace(command)
        return shlex.split(command)

    def _command(self, command: t.Union[str, Dict], **kwargs: t.Any) -> Dict:
        if isinstance(command, str):
            return {'command': command, **kwargs}
        elif isinstance(command, dict):
            kwargs.update(command)
            return kwargs
        else:
            raise Exception('`command` does not currently support variables other than `str`, `dict`')

    def _popen(self, args: t.List[str], unsafe: bool) -> s.Popen:
        cmd = ' '.join(args) if unsafe else args
        return s.Popen(cmd, cwd=self._foam.destination, shell=unsafe, stdout=s.PIPE)
