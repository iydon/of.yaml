__all__ = ['Information']


from ...core import Foam


class Information:
    '''OpenFOAM information wrapper'''

    Self = __qualname__

    def __init__(self, foam: Foam) -> None:
        self._foam = foam

    @classmethod
    def from_foam(cls, foam: Foam) -> Self:
        return cls(foam)
