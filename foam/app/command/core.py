__all__ = ['Command']


import shlex
import shutil
import subprocess as s
import typing as t
import warnings as w

from .adapter import Default, Apps
from ...base.type import Any, DictStr, DictStrAny, ListFloat, ListInt, ListStr, SetPath
from ...compat.functools import cached_property
from ...util.function import deprecated_classmethod

if t.TYPE_CHECKING:
    import typing_extensions as te

    from ...base.core import Foam


class Command:
    '''OpenFOAM command wrapper'''

    def __init__(self, foam: 'Foam') -> None:
        self._foam = foam

    @classmethod
    def fromFoam(cls, foam: 'Foam') -> 'te.Self':
        foam.destination  # assert dest is not None
        return cls.fromFoamWithoutAsserting(foam)

    @classmethod
    def fromFoamWithoutAsserting(cls, foam: 'Foam') -> 'te.Self':
        return cls(foam)

    @property
    def times(self) -> ListFloat:
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
    def logs(self) -> SetPath:
        '''Log files'''
        logs = set()
        for path in self._foam.destination.iterdir():
            if path.stem == 'log':
                logs.add(path)
        return logs

    @cached_property
    def macros(self) -> DictStr[str]:
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
    ) -> ListInt:
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
        commands: t.List[t.Union[str, DictStrAny]],
        suffix: str = '', overwrite: bool = False, exception: bool = True,
        parallel: bool = True, unsafe: bool = False,
    ) -> ListInt:
        '''Inspired by `runApplication` and `runParallel`

        Reference:
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/bin/tools/RunFunctions
        '''
        codes: ListInt = [-1] * len(commands)
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
            App: t.Callable[['Foam'], Default] \
                = lambda foam: Apps.get(raws[0], Default)(foam, raws[0])
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

    def _split(self, command: str, parallel: bool, replace: bool = True) -> ListStr:
        if parallel and '__app__' in command:
            command = f'mpirun -np __procs__ {command} -parallel'
        if replace:
            command = self._replace(command)
        return shlex.split(command)

    def _command(self, command: t.Union[str, DictStrAny], **kwargs: Any) -> DictStrAny:
        if isinstance(command, str):
            return {'command': command, **kwargs}
        elif isinstance(command, dict):
            kwargs.update(command)
            return kwargs
        else:
            raise Exception('`command` does not currently support variables other than `str`, `dict`')

    def _popen(self, args: ListStr, unsafe: bool) -> s.Popen:
        cmd = ' '.join(args) if unsafe else args
        return s.Popen(cmd, cwd=self._foam.destination, shell=unsafe, stdout=s.PIPE)

    from_foam = deprecated_classmethod(fromFoam)
    from_foam_without_asserting = deprecated_classmethod(fromFoamWithoutAsserting)
