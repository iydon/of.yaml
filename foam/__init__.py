__all__ = ['app', 'Foam']


import functools as f
import typing as t

from . import compat


for obj, name in [
    (f, 'cached_property'),
    (f, 'singledispatchmethod'),
    (t, 'Self'),
]:
    if not hasattr(obj, name):
        setattr(obj, name, getattr(getattr(compat, obj.__name__), name))


from . import app
from .base.core import Foam


__doc__ = Foam.__doc__
__version__ = Foam.__version__
