__all__ = ['CaseBase', 'CaseParameter']


import abc
import copy
import pathlib as p
import typing as t

from ..object.data import Data
from ..function import deprecated_classmethod, dict_without_keys
from ...base.type import DictStrAny, Func1, Path

if t.TYPE_CHECKING:
    import typing_extensions as te

    from ...base.core import Foam

    P = te.ParamSpec('P')
    Kwargs = te.ParamSpecKwargs(P)


class CaseBase(abc.ABC):
    '''Case abstract class

    Example:
        ```
        class CaseCavity(CaseBase):
            __template__ = 'foam/static/demo/7/cavity.yaml'

            @property
            def t(self) -> float:
                return self._required['t']

            def optional(self):
                pass

            def required(self, t: float, dt: float):
                return self.dict_without_keys(vars(), 'te.self')

            def finalize(self, foam, optional, required):
                foam['foam'].set_via_dict({
                    'system': {
                        'controlDict': {
                            'endTime': self.t,
                            'deltaT': required['dt'],
                        },
                    },
                })
        ```

        >>> case_template = CaseCavity.new(t=0.3, dt=0.005)
        >>> print(case_template)
        CaseCavity(t=0.3, dt=0.005) \\
            .set_optional() \\
            .set_optional(t=0.3, dt=0.005)
        >>> for t in [0.3, 0.4, 0.5]:
        ...     parts = 'case', str(t)
        ...     case = case_template \\
        ...         .copy(deepcopy=False) \\
        ...         .set_required(t=t) \\
        ...         .save(*parts)
        ...     case.parameter.dump_to_path(*parts, 'meta.json')
        ...     codes = case.foam.cmd.all_run(overwrite=False)
        ...     print(codes)
        [0, 0]
        [0, 0]
        [0, 0]
    '''

    __slots__ = ('_foam', '_kwargs', '_optional', '_required')
    __template__ = None

    dict_without_keys = staticmethod(dict_without_keys)

    def __init__(self, **kwargs: 'Kwargs') -> None:
        from ...base.core import Foam

        self._foam = Foam.fromPath(self.tempalte)
        self._kwargs = kwargs
        self._optional = self.optional() or {}
        self._required = self.required(**kwargs) or {}

    def __repr__(self) -> str:
        func: Func1[DictStrAny, str] \
            = lambda d: ', '.join(f'{k}={v!r}' for k, v in d.items())
        return f'{self.__class__.__name__}({func(self._kwargs)}) \\\n' \
            f'    .set_optional({func(self._optional)}) \\\n' \
            f'    .set_required({func(self._required)})'

    @classmethod
    def default(cls) -> 'te.Self':
        raise NotImplementedError

    @classmethod
    def new(cls, **kwargs: 'Kwargs') -> 'te.Self':
        return cls(**kwargs)

    @abc.abstractmethod
    def optional(self) -> t.Optional[DictStrAny]:
        '''Initialize optional properties'''
        pass

    @abc.abstractmethod
    def required(self, **kwargs: 'Kwargs') -> t.Optional[DictStrAny]:
        '''Initialize required properties'''
        pass

    @abc.abstractmethod
    def finalize(self, foam: 'Foam', optional: DictStrAny, required: DictStrAny) -> t.Optional['Foam']:
        '''Convert class properties to case parameters'''
        pass

    @property
    def foam(self) -> 'Foam':
        return self._foam

    @property
    def data(self) -> 'Data':
        return self._foam['foam']

    @property
    def tempalte(self) -> p.Path:
        assert self.__template__ is not None, f'Can\'t instantiate abstract class {self.__class__.__name__} with abstract variable __template__'

        return p.Path(self.__template__)

    @property
    def parameter(self) -> 'CaseParameter':
        return CaseParameter(self._optional, self._required)

    def copy(self, deepcopy: bool = False) -> 'te.Self':
        if deepcopy:
            return copy.deepcopy(self)
        else:
            return self.__class__(**self._kwargs) \
                .set_optional(**self._optional) \
                .set_required(**self._required)

    def set_from_path(self, *parts: str) -> 'te.Self':
        parameter = CaseParameter.loadFromPath(*parts)
        return self \
            .set_optional(**parameter.optional) \
            .set_required(**parameter.required)

    def set_optional(self, **kwargs: 'Kwargs') -> 'te.Self':
        self._optional.update(kwargs)
        return self

    def set_required(self, **kwargs: 'Kwargs') -> 'te.Self':
        self._required.update(kwargs)
        return self

    def save(self, *parts: str) -> 'te.Self':
        foam = self.finalize(self._foam, self._optional, self._required)
        if foam is not None:
            self._foam = foam
        self._foam.save(p.Path(*map(str, parts)))
        return self


class CaseParameter(t.NamedTuple):
    '''Parameter for case'''

    optional: DictStrAny
    required: DictStrAny

    @classmethod
    def loadFromPath(cls, *parts: str) -> 'te.Self':
        data = Data.loadFromPath(*parts)
        return cls(optional=data.get('optional', {}), required=data.get('required', {}))

    def dump(self, *paths: Path) -> 'te.Self':
        self._data().dump(*paths)
        return self

    def dump_to_path(self, *parts: str) -> 'te.Self':
        return self.dump(p.Path(*parts))

    def _data(self) -> 'Data':
        return Data.fromDict({'optional': self.optional, 'required': self.required})

    load_from_path = deprecated_classmethod(loadFromPath)
