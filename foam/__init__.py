import functools as _functools
import shutil as _shutil

from . import compat as _compat


_functools.cached_property = _compat.functools.cached_property
_functools.singledispatchmethod = _compat.functools.singledispatchmethod
_shutil.copytree = _compat.shutil.copytree


import importlib as _importlib

from .namespace import *


__import__ = lambda name: _importlib.import_module(name, __name__)
__all__ = __import__('.namespace').__all__
__doc__ = Foam.__doc__
__license__ = __import__('.util').function.license(full_text=False)
__version__ = Foam.__version__
