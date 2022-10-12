__all__ = ['lib']


import types
import typing as t
import warnings as w

from ..base.type import CachedLib


class lib:
    '''Load modules on demand'''

    _cache: t.Dict[str, CachedLib] = {}

    def __class_getitem__(cls, key: str) -> t.Optional[CachedLib]:
        if key in cls._cache:
            ans = cls._cache[key]
        else:
            attr = getattr(cls, key)
            try:
                ans = attr()
            except (ModuleNotFoundError, ImportError) as e:
                ans = None
                w.warn(f'{e.msg} ({attr.__doc__})')
            cls._cache[key] = ans
        return ans

    @classmethod
    def reset(cls) -> type:
        cls._cache.clear()
        return cls

    @classmethod
    def click(cls) -> types.ModuleType:
        '''https://pypi.org/project/click'''
        import click

        return click

    @classmethod
    def lark(cls) -> types.ModuleType:
        '''https://pypi.org/project/lark'''
        import lark

        return lark

    @classmethod
    def numpy(cls) -> types.ModuleType:
        '''https://pypi.org/project/numpy'''
        import numpy

        return numpy

    @classmethod
    def py7zr(cls) -> types.ModuleType:
        '''https://pypi.org/project/py7zr'''
        import py7zr

        return py7zr

    @classmethod
    def tqdm(cls) -> types.ModuleType:
        '''https://pypi.org/project/tqdm'''
        import tqdm

        return tqdm

    @classmethod
    def vtk(cls) -> types.ModuleType:
        '''https://pypi.org/project/vtk'''
        import vtkmodules.all as vtk

        return vtk

    @classmethod
    def yaml(cls) -> types.ModuleType:
        '''https://pypi.org/project/PyYAML'''
        import yaml

        return yaml

    @classmethod
    def SafeLoader(cls) -> object:
        '''https://pypi.org/project/PyYAML'''
        try:
            from yaml import CSafeLoader as SafeLoader
        except ImportError:
            from yaml import SafeLoader

        return SafeLoader

    @classmethod
    def vtk_to_numpy(cls) -> t.Callable:
        '''https://pypi.org/project/vtk'''
        from vtkmodules.util.numpy_support import vtk_to_numpy

        return vtk_to_numpy
