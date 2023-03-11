__all__ = ['Case']


import typing as t

from ..base.type import Any, DictStrAny, ListAny
from ..compat.functools import singledispatchmethod
from ..util.implementation import Singleton


class Case(Singleton):
    '''OpenFOAM case parser

    Example:
        >>> data = {
        ...     'FoamFile': {
        ...         'version': 2.0,
        ...         'format': 'ascii',
        ...         'class': 'volVectorField',
        ...         'object': 'U',
        ...     },
        ...     'dimensions': '[0 1 -1 0 0 0 0]',
        ...     'internalField': 'uniform (0 0 0)',
        ...     'boundaryField': {
        ...         'movingWall': {
        ...             'type': 'fixedValue',
        ...             'value': 'uniform (1 0 0)',
        ...         },
        ...         'fixedWalls': {'type': 'noSlip'},
        ...         'frontAndBack': {'type': 'empty'},
        ...     },
        ... }
        >>> case = Case.default()
        >>> print('\\n'.join(case.data(data)))
        FoamFile {version 2.0; format ascii; class volVectorField; object U;}
        dimensions [0 1 -1 0 0 0 0];
        internalField uniform (0 0 0);
        boundaryField {movingWall {type fixedValue; value uniform (1 0 0);} fixedWalls {type noSlip;} frontAndBack {type empty;}}
    '''

    def data(self, data: DictStrAny) -> t.Iterator[str]:
        for key, value in data.items():
            yield f'{self.key(key)} {self.value(value)}'

    def key(self, key: str) -> str:
        key = key.replace(' ', '')  # div(phi, U) -> div(phi,U)
        if any(c in key for c in '()*|'):  # (U|k|epsilon) -> "(U|k|epsilon)"
            key = f'"{key}"'
        return key

    @singledispatchmethod
    def value(self, value: Any) -> str:
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
    def _(self, value: ListAny) -> str:
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
    def _(self, value: DictStrAny) -> str:
        string = ' '.join(self.data(value))
        return f'{{{string}}}'
