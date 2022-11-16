__all__ = ['Version']


import typing as t

from ..function import deprecated_classmethod

if t.TYPE_CHECKING:
    from typing_extensions import Self


class Version(t.NamedTuple):
    '''Version named tuple

    Example:
        >>> version = Version.fromString('1.2.x')
        >>> version.major, version.minor, version.other, version.micro
        (1, 2, 'x', None)
        >>> version.to_string()
        '1.2.x'
    '''

    major: int
    minor: int
    other: t.Optional[str]

    def __lt__(self, other: 'Self') -> bool:
        return (self.major, self.minor) < (other.major, other.minor)

    def __gt__(self, other: 'Self') -> bool:
        return other.__lt__(self)

    def __repr__(self) -> str:
        return f'Version.fromString({self.to_string()!r})'

    def __str__(self) -> str:
        return self.to_string()

    @classmethod
    def fromString(cls, version: str) -> 'Self':
        parts = version.split('.', maxsplit=2)
        if len(parts) == 2:
            major, minor = parts
            other = None
        elif len(parts) == 3:
            major, minor, other = parts
        else:
            raise Exception(f'"{version}" is not a valid version string')
        return cls(int(major), int(minor), other)

    @property
    def micro(self) -> t.Optional[int]:
        if self.other is not None:
            parts = self.other.split('.')
            if parts and parts[0].isdigit():
                return int(parts[0])
        return None

    @property
    def micro_int(self) -> int:
        return self.micro or 0

    def to_string(self) -> str:
        version = f'{self.major}.{self.minor}'
        if self.other is not None:
            version += f'.{self.other}'
        return version

    from_string = deprecated_classmethod(fromString)
