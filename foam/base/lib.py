__all__ = ['lib']


import types
import typing as t
import warnings as w

from .type import CachedLib


class lib:
    '''Load modules on demand'''

    _cache: t.Dict[str, CachedLib] = {}

    def __class_getitem__(cls, key: str) -> t.Optional[CachedLib]:
        if key in cls._cache:
            return cls._cache[key]
        for prefix in {'mod', 'cls', 'func'}:
            name = f'{prefix}_{key}'
            if hasattr(cls, name):
                attr = getattr(cls, name)
                try:
                    ans = attr()
                except (ModuleNotFoundError, ImportError) as e:
                    ans = None
                    w.warn(f'{e.msg} ({attr.__doc__})')
                else:
                    cls._cache[key] = ans
                return ans
        raise KeyError(key)

    @classmethod
    def reset(cls) -> type:
        cls._cache.clear()
        return cls

    @classmethod
    def mod_click(cls) -> types.ModuleType:
        '''https://pypi.org/project/click'''
        import click

        return click

    @classmethod
    def mod_numpy(cls) -> types.ModuleType:
        '''https://pypi.org/project/numpy'''
        import numpy

        return numpy

    @classmethod
    def mod_py7zr(cls) -> types.ModuleType:
        '''https://pypi.org/project/py7zr'''
        import py7zr

        return py7zr

    @classmethod
    def mod_tqdm(cls) -> types.ModuleType:
        '''https://pypi.org/project/tqdm'''
        import tqdm

        return tqdm

    @classmethod
    def mod_vtk(cls) -> types.ModuleType:
        '''https://pypi.org/project/vtk'''
        import vtkmodules.all as vtk

        return vtk

    @classmethod
    def mod_yaml(cls) -> types.ModuleType:
        '''https://pypi.org/project/PyYAML'''
        import yaml

        return yaml

    @classmethod
    def cls_SafeLoader(cls) -> object:
        '''https://pypi.org/project/PyYAML'''
        try:
            from yaml import CSafeLoader as SafeLoader
        except ImportError:
            from yaml import SafeLoader

        return SafeLoader

    @classmethod
    def func_vtk_to_numpy(cls) -> t.Callable:
        '''https://pypi.org/project/vtk'''
        from vtkmodules.util.numpy_support import vtk_to_numpy

        return vtk_to_numpy
