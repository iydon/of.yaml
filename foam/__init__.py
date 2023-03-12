import importlib as _importlib
import typing as _typing

from .namespace.brief import *
from .base.type import ModuleType as _ModuleType


__import__: _typing.Callable[[str], _ModuleType] \
    = lambda name: _importlib.import_module(name, __name__)
__all__ = __import__('.namespace.brief').__all__
__doc__ = Foam.__doc__
__license__ = __import__('.util.function').license(full_text=False)
__version__ = Foam.__version__
