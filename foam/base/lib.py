__all__ = ['classproperty', 'lark', 'matplotlib', 'numpy', 'py7zr', 'tomlkit', 'tqdm', 'vtkmodules', 'yaml']


import typing as t

from .type import Any, FuncAny2

if t.TYPE_CHECKING:
    import typing_extensions as te

    import lark as _lark
    import matplotlib as _matplotlib
    import matplotlib.figure as _figure
    import matplotlib.pyplot as _pyplot
    import numpy as _numpy
    import py7zr as _py7zr
    import tomlkit as _tomlkit
    import tqdm as _tqdm
    import vtkmodules as _vtkmodules
    import yaml as _yaml

    P = te.ParamSpec('P')


class classproperty:
    '''Decorator that converts a method with a single cls argument into a property that can be accessed directly from the class.

    Reference:
        - https://github.com/django/django

    TODO:
        - place it in util::decorator will cause circular import problem
    '''

    def __init__(self, method: t.Optional[FuncAny2] = None) -> None:
        self.fget = method

    def __get__(self, instance: Any, cls: t.Optional[type] = None) -> Any:
        return self.fget(cls)

    def getter(self, method: FuncAny2) -> 'te.Self':
        self.fget = method
        return self


class lark:
    '''pip install ifoam[lark]'''

    @classmethod
    def Lark(cls, *args: 'P.args', **kwargs: 'P.kwargs') -> '_lark.Lark':
        return cls._().Lark(*args, **kwargs)

    @classmethod
    def _(cls) -> '_lark':
        try:
            import lark
        except Exception as e:
            raise e.__class__(cls.__doc__)
        else:
            return lark


class matplotlib:
    '''pip install ifoam[mpl]'''

    @classproperty
    def figure(cls) -> '_figure':
        return cls._().figure

    @classproperty
    def pyplot(cls) -> '_pyplot':
        return cls._().pyplot

    @classmethod
    def _(cls) -> '_matplotlib':
        try:
            import matplotlib
            import matplotlib.figure
            import matplotlib.pyplot
        except Exception as e:
            raise e.__class__(cls.__doc__)
        else:
            return matplotlib


class numpy:
    '''pip install ifoam[vtk]'''

    @classmethod
    def argmin(cls, *args: 'P.args', **kwargs: 'P.kwargs') -> '_numpy.ndarray':
        return cls._().argmin(*args, **kwargs)

    @classmethod
    def loadtxt(cls, *args: 'P.args', **kwargs: 'P.kwargs') -> '_numpy.ndarray':
        return cls._().loadtxt(*args, **kwargs)

    @classmethod
    def square(cls, *args: 'P.args', **kwargs: 'P.kwargs') -> '_numpy.ndarray':
        return cls._().square(*args, **kwargs)

    @classmethod
    def _(cls) -> '_numpy':
        try:
            import numpy
        except Exception as e:
            raise e.__class__(cls.__doc__)
        else:
            return numpy


class py7zr:
    '''pip install ifoam[7z]'''

    @classmethod
    def SevenZipFile(cls, *args: 'P.args', **kwargs: 'P.kwargs') -> '_py7zr.SevenZipFile':
        return cls._().SevenZipFile(*args, **kwargs)

    @classmethod
    def _(cls) -> '_py7zr':
        try:
            import py7zr
        except Exception as e:
            raise e.__class__(cls.__doc__)
        else:
            return py7zr


class tomlkit:
    '''pip install ifoam[toml]'''

    @classmethod
    def dump(cls, *args: 'P.args', **kwargs: 'P.kwargs') -> None:
        cls._().dump(*args, **kwargs)

    @classmethod
    def dumps(cls, *args: 'P.args', **kwargs: 'P.kwargs') -> str:
        return cls._().dumps(*args, **kwargs)

    @classmethod
    def load(cls, *args: 'P.args', **kwargs: 'P.kwargs') -> '_tomlkit.toml_document.TOMLDocument':
        return cls._().load(*args, **kwargs)

    @classmethod
    def loads(cls, *args: 'P.args', **kwargs: 'P.kwargs') -> Any:
        return cls._().loads(*args, **kwargs)

    @classmethod
    def _(cls) -> '_tomlkit':
        try:
            import tomlkit
        except Exception as e:
            raise e.__class__(cls.__doc__)
        else:
            return tomlkit


class tqdm:
    '''pip install ifoam[tqdm]'''

    @classmethod
    def is_available(cls) -> bool:
        try:
            cls._()
        except Exception:
            return False
        else:
            return True

    @classmethod
    def is_not_available(cls) -> bool:
        return not cls.is_available()

    @classmethod
    def tqdm(cls, *args: 'P.args', **kwargs: 'P.kwargs') -> '_tqdm.std.tqdm':
        return cls._().tqdm(*args, **kwargs)

    @classmethod
    def _(cls) -> '_tqdm':
        try:
            import tqdm
        except Exception as e:
            raise e.__class__(cls.__doc__)
        else:
            return tqdm


class vtkmodules:
    '''pip install ifoam[vtk]'''

    @classmethod
    def vtkGenericDataObjectReader(cls, *args: 'P.args', **kwargs: 'P.kwargs') -> '_vtkmodules.vtkIOLegacy.vtkGenericDataObjectReader':
        return cls._().vtkIOLegacy.vtkGenericDataObjectReader()

    @classmethod
    def vtk_to_numpy(cls, *args: 'P.args', **kwargs: 'P.kwargs') -> '_numpy.ndarray':
        try:
            from vtkmodules.util.numpy_support import vtk_to_numpy
        except Exception as e:
            raise e.__class__(cls.__doc__)
        else:
            return vtk_to_numpy(*args, **kwargs)

    @classmethod
    def _(cls) -> '_vtkmodules':
        try:
            import vtkmodules.all
        except Exception as e:
            raise e.__class__(cls.__doc__)
        else:
            return vtkmodules


class yaml:
    '''pip install ifoam'''

    @classmethod
    def dump(cls, *args: 'P.args', **kwargs: 'P.kwargs') -> str:
        kwargs = {'Dumper': cls._dumper(), **kwargs}
        return cls._().dump(*args, **kwargs)

    @classmethod
    def dump_all(cls, *args: 'P.args', **kwargs: 'P.kwargs') -> str:
        kwargs = {'Dumper': cls._dumper(), **kwargs}
        return cls._().dump_all(*args, **kwargs)

    @classmethod
    def load(cls, *args: 'P.args', **kwargs: 'P.kwargs') -> Any:
        kwargs = {'Loader': cls._loader(), **kwargs}
        return cls._().load(*args, **kwargs)

    @classmethod
    def load_all(cls, *args: 'P.args', **kwargs: 'P.kwargs') -> t.Iterator[Any]:
        kwargs = {'Loader': cls._loader(), **kwargs}
        return cls._().load_all(*args, **kwargs)

    @classmethod
    def _(cls) -> '_yaml':
        try:
            import yaml
        except Exception as e:
            raise e.__class__(cls.__doc__)
        else:
            return yaml

    @classmethod
    def _dumper(cls) -> t.Union['_yaml.SafeDumper', '_yaml.CSafeDumper']:
        yaml = cls._()
        if yaml.__with_libyaml__:
            return yaml.CSafeDumper
        else:
            return yaml.SafeDumper

    @classmethod
    def _loader(cls) -> t.Union['_yaml.SafeLoader', '_yaml.CSafeLoader']:
        yaml = cls._()
        if yaml.__with_libyaml__:
            return yaml.CSafeLoader
        else:
            return yaml.SafeLoader
