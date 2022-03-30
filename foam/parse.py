__all__ = ['Parse']


import functools as f
import typing as t

if t.TYPE_CHECKING:
    from . import Foam
    from .type import Dict


class Parse:
    '''OpenFOAM YAML parser'''

    def __init__(self, foam: 'Foam') -> None:
        self._foam = foam

    def data(self, data: 'Dict') -> t.Iterator[str]:
        for key, value in data.items():
            yield f'{self.key(key)} {self.value(value)}'

    def key(self, key: str) -> str:
        key = key.replace(' ', '')  # div(phi, U) -> div(phi,U)
        if any(c in key for c in '()*'):  # (U|k|epsilon) -> "(U|k|epsilon)"
            key = f'"{key}"'
        return key

    @f.singledispatchmethod
    def value(self, value: t.Any) -> str:
        raise Exception(f'Unknown type "{type(value).__name__}"')

    @value.register(bool)
    def _(self, value: bool) -> str:
        return f'{str(value).lower()};'

    @value.register(str)
    @value.register(int)
    @value.register(float)
    def _(self, value: t.Union[str, int, float]) -> str:
        return f'{value};'

    @value.register(list)
    def _(self, value: t.List[t.Any]) -> str:
        T = type(value[0]) if value else None
        if T in {str, int, float}:
            return f'({" ".join(map(str, value))});'
        elif T is dict:
            strings = []
            for element in value:
                head = tuple(k for k, v in element.items() if v is None)
                if head:
                    element.pop(head[0])
                    string = ' '.join(self.data(element))
                    strings.append(f'{head[0]} {{{string}}}')
                else:
                    string = ' '.join(self.data(element))
                    strings.append(f'{{{string}}}')
            return f'({" ".join(strings)});'
        else:
            raise Exception(f'Unknown list "{value}"')

    @value.register(dict)
    def _(self, value: 'Dict') -> str:
        string = ' '.join(self.data(value))
        return f'{{{string}}}'
