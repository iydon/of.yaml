__all__ = ['app', 'Foam']


import functools as f

from . import compat


f.cached_property = compat.functools.cached_property
f.singledispatchmethod = compat.functools.singledispatchmethod


from . import app
from .base.core import Foam


__doc__ = Foam.__doc__
__version__ = Foam.__version__
