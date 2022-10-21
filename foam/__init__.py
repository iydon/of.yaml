__all__ = ['app', 'util', 'Foam']


import functools as f

from . import compat


f.cached_property = compat.functools.cached_property
f.singledispatchmethod = compat.functools.singledispatchmethod


from . import app, util
from .base.core import Foam


__doc__ = Foam.__doc__
__license__ = util.function.license(full_text=False)
__version__ = Foam.__version__
