__all__ = ['YAML']


import functools as f
import typing as t

from ..base.type import Dict

if t.TYPE_CHECKING:
    from typing_extensions import Self


class YAML:
    '''OpenFOAM YAML parser'''

    _instance = None

    @classmethod
    def default(cls) -> 'Self':
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def data(self, data: Dict) -> t.Iterator[str]:
        for key, value in data.items():
            yield f'{self.key(key)} {self.value(value)}'

    def key(self, key: str) -> str:
        key = key.replace(' ', '')  # div(phi, U) -> div(phi,U)
        if any(c in key for c in '()*|'):  # (U|k|epsilon) -> "(U|k|epsilon)"
            key = f'"{key}"'
        return key

    @f.singledispatchmethod
    def value(self, value: t.Any) -> str:
        raise Exception(f'Unknown type "{type(value).__name__}"')

    @value.register(bool)
    def _(self, value: bool) -> str:
        return f'{str(value).lower()};'

    @value.register(float)
    @value.register(int)
    @value.register(str)
    def _(self, value: t.Union[str, int, float]) -> str:
        return f'{value};'

    @value.register(list)
    def _(self, value: t.List[t.Any]) -> str:
        if not value or isinstance(value[0], (str, int, float)):
            return f'({" ".join(map(str, value))});'
        elif isinstance(value[0], dict):
            strings = []
            for element in value:
                head = tuple(k for k, v in element.items() if v is None)
                if head:
                    element_cloned = element.copy()
                    element_cloned.pop(head[0])
                    string = ' '.join(self.data(element_cloned))
                    strings.append(f'{head[0]} {{{string}}}')
                else:
                    string = ' '.join(self.data(element))
                    strings.append(f'{{{string}}}')
            return f'({" ".join(strings)});'
        else:
            raise Exception(f'Unknown list "{value}"')

    @value.register(dict)
    def _(self, value: Dict) -> str:
        string = ' '.join(self.data(value))
        return f'{{{string}}}'
