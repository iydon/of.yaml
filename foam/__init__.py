__all__ = ['app', 'Foam']


import functools as f

from . import compat


for obj, name in [
    (f, 'cached_property'),
    (f, 'singledispatchmethod'),
]:
    if not hasattr(obj, name):
        setattr(obj, name, getattr(getattr(compat, obj.__name__), name))


from . import app
from .base.core import Foam


__doc__ = Foam.__doc__
__version__ = Foam.__version__
