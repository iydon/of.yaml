__all__ = ['lib']


import types
import typing as t
import warnings as w

from .type import CachedLib


class Lib:
    def __init__(self) -> None:
        self._cache: t.Dict[str, CachedLib] = {}

    def __class_getitem__(self, key: str) -> t.Optional[CachedLib]:
        # TODO
        raise NotImplementedError

    def __getitem__(self, key: str) -> t.Optional[CachedLib]:
        if key in self._cache:
            return self._cache[key]
        for prefix in {'mod', 'cls', 'func'}:
            name = f'{prefix}_{key}'
            if hasattr(self, name):
                attr = getattr(self, name)
                try:
                    ans = attr()
                except (ModuleNotFoundError, ImportError) as e:
                    ans = None
                    w.warn(f'{e.msg} ({attr.__doc__})')
                else:
                    self._cache[key] = ans
                return ans
        raise KeyError(key)

    @classmethod
    def default(cls) -> t.Self:
        return cls()

    def reset(self) -> t.Self:
        self._cache.clear()
        return self

    def mod_click(self) -> types.ModuleType:
        '''https://pypi.org/project/click'''
        import click

        return click

    def mod_numpy(self) -> types.ModuleType:
        '''https://pypi.org/project/numpy'''
        import numpy

        return numpy

    def mod_py7zr(self) -> types.ModuleType:
        '''https://pypi.org/project/py7zr'''
        import py7zr

        return py7zr

    def mod_tqdm(self) -> types.ModuleType:
        '''https://pypi.org/project/tqdm'''
        import tqdm

        return tqdm

    def mod_vtk(self) -> types.ModuleType:
        '''https://pypi.org/project/vtk'''
        import vtkmodules.all as vtk

        return vtk

    def mod_yaml(self) -> types.ModuleType:
        '''https://pypi.org/project/PyYAML'''
        import yaml

        return yaml

    def cls_SafeLoader(self) -> object:
        '''https://pypi.org/project/PyYAML'''
        try:
            from yaml import CSafeLoader as SafeLoader
        except ImportError:
            from yaml import SafeLoader

        return SafeLoader

    def func_vtk_to_numpy(self) -> t.Callable:
        '''https://pypi.org/project/vtk'''
        from vtkmodules.util.numpy_support import vtk_to_numpy

        return vtk_to_numpy


lib = Lib.default()
