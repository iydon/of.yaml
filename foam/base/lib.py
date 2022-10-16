__all__ = ['lark', 'numpy', 'py7zr', 'tqdm', 'vtkmodules', 'yaml']


import typing as t

if t.TYPE_CHECKING:
    import lark as _lark
    import numpy as _numpy
    import py7zr as _py7zr
    import tqdm as _tqdm
    import vtkmodules as _vtkmodules
    import yaml as _yaml


class lark:
    '''pip install ifoam[lark]'''

    @classmethod
    def Lark(cls, *args: t.Any, **kwargs: t.Any) -> '_lark.Lark':
        return cls._().Lark(*args, **kwargs)

    @classmethod
    def _(cls) -> '_lark':
        try:
            import lark
        except Exception as e:
            raise e.__class__(cls.__doc__)

        return lark



class numpy:
    '''pip install ifoam[vtk]'''

    @classmethod
    def argmin(cls, *args: t.Any, **kwargs: t.Any) -> '_numpy.ndarray':
        return cls._().argmin(*args, **kwargs)

    @classmethod
    def loadtxt(cls, *args: t.Any, **kwargs: t.Any) -> '_numpy.ndarray':
        return cls._().loadtxt(*args, **kwargs)

    @classmethod
    def square(cls, *args: t.Any, **kwargs: t.Any) -> '_numpy.ndarray':
        return cls._().square(*args, **kwargs)

    @classmethod
    def _(cls) -> '_numpy':
        try:
            import numpy
        except Exception as e:
            raise e.__class__(cls.__doc__)

        return numpy


class py7zr:
    '''pip install ifoam[7z]'''

    @classmethod
    def SevenZipFile(cls, *args: t.Any, **kwargs: t.Any) -> '_py7zr.SevenZipFile':
        return cls._().SevenZipFile(*args, **kwargs)

    @classmethod
    def _(cls) -> '_py7zr':
        try:
            import py7zr
        except Exception as e:
            raise e.__class__(cls.__doc__)

        return py7zr


class tqdm:
    '''pip install ifoam[tqdm]'''

    @classmethod
    def is_available(cls) -> bool:
        try:
            cls._()
        except:
            return False
        else:
            return True

    @classmethod
    def is_not_available(cls) -> bool:
        return not cls.is_available()

    @classmethod
    def tqdm(cls, *args: t.Any, **kwargs: t.Any) -> '_tqdm.std.tqdm':
        return cls._().tqdm(*args, **kwargs)

    @classmethod
    def _(cls) -> '_tqdm':
        try:
            import tqdm
        except Exception as e:
            raise e.__class__(cls.__doc__)

        return tqdm


class vtkmodules:
    '''pip install ifoam[vtk]'''

    @classmethod
    def vtkGenericDataObjectReader(cls, *args: t.Any, **kwargs: t.Any) -> '_vtkmodules.vtkIOLegacy.vtkGenericDataObjectReader':
        return cls._().vtkIOLegacy.vtkGenericDataObjectReader()

    @classmethod
    def vtk_to_numpy(cls, *args: t.Any, **kwargs: t.Any) -> '_numpy.ndarray':
        try:
            from vtkmodules.util.numpy_support import vtk_to_numpy
        except Exception as e:
            raise e.__class__(cls.__doc__)

        return vtk_to_numpy(*args, **kwargs)

    @classmethod
    def _(cls) -> '_vtkmodules':
        try:
            import vtkmodules.all
        except Exception as e:
            raise e.__class__(cls.__doc__)

        return vtkmodules


class yaml:
    '''pip install ifoam'''

    @classmethod
    def dump_all(cls, *args: t.Any, **kwargs: t.Any) -> str:
        return cls._().dump_all(*args, **kwargs)

    @classmethod
    def load(cls, *args: t.Any, **kwargs: t.Any) -> t.Any:
        kwargs['Loader'] = cls._loader()
        return cls._().load(*args, **kwargs)

    @classmethod
    def load_all(cls, *args: t.Any, **kwargs: t.Any) -> t.Iterator[t.Any]:
        kwargs['Loader'] = cls._loader()
        return cls._().load_all(*args, **kwargs)

    @classmethod
    def _(cls) -> '_yaml':
        try:
            import yaml
        except Exception as e:
            raise e.__class__(cls.__doc__)

        return yaml

    @classmethod
    def _loader(cls) -> t.Union['_yaml.SafeLoader', '_yaml.CSafeLoader']:
        yaml = cls._()
        if yaml.__with_libyaml__:
            return yaml.CSafeLoader
        else:
            return yaml.SafeLoader
