import importlib as _importlib

from .namespace.brief import *
from .base.type import Func1 as _Func1, ModuleType as _ModuleType


__import__: _Func1[str, _ModuleType] \
    = lambda name: _importlib.import_module(name, __name__)
__all__ = __import__('.namespace.brief').__all__
__doc__ = Foam.__doc__
__license__ = __import__('.util.function').license(full_text=False)
__version__ = Foam.__version__
