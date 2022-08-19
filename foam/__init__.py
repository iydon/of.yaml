__all__ = ['app', 'Foam']


import functools as f

from . import app, compat
from .base import Foam


__doc__ = Foam.__doc__
__version__ = Foam.__version__

for obj, name in [
    (f, 'cached_property'),
    (f, 'singledispatchmethod'),
]:
    if not hasattr(obj, name):
        setattr(obj, name, getattr(getattr(compat, obj.__name__), name))
