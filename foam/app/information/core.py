__all__ = ['Information']


import collections as c
import os
import pathlib as p
import re
import typing as t

from ...base.type import Path

if t.TYPE_CHECKING:
    from typing_extensions import Self

    from ..command.core import Command
    from ...base.core import Foam


class Information:
    '''OpenFOAM information wrapper'''

    def __init__(self, foam: 'Foam') -> None:
        self._foam = foam
        self._cmd: t.Optional['Command'] = None

    @classmethod
    def from_foam(cls, foam: 'Foam') -> 'Self':
        return cls(foam)

    @classmethod
    def default(cls) -> 'Self':
        from ...base.core import Foam

        return cls(Foam.default())

    @property
    def cmd(self) -> 'Command':
        '''Command without asserting (no need to call `Foam::save` method first)'''
        from ..command.core import Command

        if self._cmd is None:
            self._cmd = Command.from_foam_without_asserting(self._foam)
        return self._cmd

    @property
    def environ(self) -> t.Dict[str, str]:
        '''OpenFOAM environments (aliase for `Foam::environ` property)'''
        if self._foam is not None:  # True
            return self._foam.environ
        else:
            return {
                key: value
                for key, value in os.environ.items()
                if any(key.startswith(p) for p in ['FOAM_', 'WM_'])
            }

    @property
    def root(self) -> p.Path:
        return p.Path(self.environ['WM_PROJECT_DIR'])

    @property
    def shared_libraries(self) -> t.Set[str]:
        ans = set()
        pattern = re.compile(fr'{self.environ["FOAM_LIBBIN"]}.+?\.so')
        for command in self.commands(foam_only=True):
            path = self.cmd.which(command)
            if path is not None:
                stdout = self.cmd.raw(f'ldd {path}').stdout.decode()
                ans.update(pattern.findall(stdout))
        return ans

    def search(self, *targets: str, process: bool = True) -> t.Union[str, t.Set[str]]:
        '''`foamSearch` wrapper

        - Reference:
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/bin/foamSearch
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/miscellaneous/foamDictionary/foamDictionary.C
        '''
        assert len(targets) > 1

        fields = '.'.join(map(lambda string: string.replace(' ', ''), targets[1:]))
        command = f'foamSearch {self.environ["FOAM_TUTORIALS"]} {targets[0]} "{fields}"'
        stdout = self.cmd.raw(command, output=True).stdout.decode()
        if not process:
            return stdout
        try:
            return set(
                line.split(' ', maxsplit=1)[-1].rstrip(';').strip()
                for line in stdout.splitlines()
            )
        except Exception:
            return stdout

    def search_yaml(self, *targets: str, root: Path = '.') -> t.Dict[t.Hashable, t.Set[str]]:
        '''`foamSearch` in YAML

        - Note:
            - `targets` should be as detailed as possible, as it is assumed that `targets` will only appear once in a file
        '''
        from ...base.core import Foam

        assert targets

        record = c.defaultdict(set)
        hashing = lambda string: string.lower().replace(' ', '')
        hashed_targets = tuple(map(hashing, targets))
        length = len(targets)
        for path in p.Path(root).rglob('*'):
            if path.suffix in {'.yaml', '.yml'}:
                # try-except or try-except-else?
                try:
                    foam = Foam.from_file(path, warn=False)
                    for keys, _ in foam['foam'].items(with_list=False):
                        hashed_keys = tuple(map(hashing, keys))
                        if hashed_keys[-length:] == hashed_targets:
                            record[foam['foam'][keys]].add(path.absolute().as_posix())
                            break
                except Exception:  # TODO: catch specific exceptions only
                    pass
        return dict(record)

    def commands(self, foam_only: bool = True) -> t.Set[str]:
        strize = lambda command: {
            str: lambda x: x,
            dict: lambda x: x['command'],
        }[type(command)](command)
        func = lambda x: self.cmd._split(strize(x), False)[0]
        commands = set(map(func, self._foam.pipeline))
        if foam_only:
            commands = {
                command for command in commands
                if self.environ['FOAM_APPBIN'] in (self.cmd.which(command) or '')
            }
        return commands
