__all__ = ['Information']


import collections as c
import pathlib as p
import typing as t

from ...core import Foam
from ...type import Path

if t.TYPE_CHECKING:
    from ..command import Command


class Information:
    '''OpenFOAM information wrapper'''

    Self = __qualname__

    def __init__(self, foam: Foam) -> None:
        self._foam = foam
        self._cmd = None

    @classmethod
    def from_foam(cls, foam: Foam) -> Self:
        return cls(foam)

    @property
    def cmd(self) -> 'Command':
        from ..command import Command

        if self._cmd is None:
            self._cmd = Command.from_foam_without_asserting(self._foam)
        return self._cmd

    def search(self, *targets: str, process: bool = True) -> t.Union[str, t.Set[str]]:
        '''foamSearch wrapper

        - Reference:
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/bin/foamSearch
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/miscellaneous/foamDictionary/foamDictionary.C
        '''
        assert len(targets) > 1

        fields = '.'.join(map(lambda string: string.replace(' ', ''), targets[1:]))
        command = f'foamSearch {self._foam.environ["FOAM_TUTORIALS"]} {targets[0]} "{fields}"'
        stdout = self.cmd.raw(command, output=True).stdout.decode()
        if not process:
            return stdout
        try:
            return set(
                line.split(' ', maxsplit=1)[-1].strip()
                for line in stdout.splitlines()
            )
        except:
            return stdout

    def search_yaml(self, *targets: str, root: Path = '.') -> t.Dict[t.Hashable, t.Set[str]]:
        '''foamSearch in YAML

        - Note:
            - `targets` should be as detailed as possible, as it is assumed that `targets` will only appear once in a file
        '''
        assert targets

        record = c.defaultdict(set)
        hashing = lambda string: string.lower().replace(' ', '')
        hashed_targets = tuple(map(hashing, targets))
        length = len(targets)
        for path in p.Path(root).rglob('*'):
            if path.suffix in {'.yaml', '.yml'}:
                # try-except or try-except-else?
                try:
                    foam = Foam.from_file(path)
                except:  # TODO: catch ConstructorError only
                    continue
                for keys, _ in foam['foam'].items(with_list=False):
                    hashed_keys = tuple(map(hashing, keys))
                    if hashed_keys[-length:] == hashed_targets:
                        record[foam['foam'][keys]].add(path.absolute().as_posix())
                        break
        return dict(record)
