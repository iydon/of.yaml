import importlib as _importlib

from .namespace.brief import *


__import__ = lambda name: _importlib.import_module(name, __name__)
__all__ = __import__('.namespace.brief').__all__
__doc__ = Foam.__doc__
__license__ = __import__('.util.function').license(full_text=False)
__version__ = Foam.__version__
