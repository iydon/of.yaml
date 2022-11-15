__all__ = ['cached_property', 'singledispatchmethod']


import functools as f
import sys


version = (sys.version_info.major, sys.version_info.minor)
if version == (3, 7):
    from .v37 import cached_property, singledispatchmethod
elif version == (3, 8):
    cached_property = f.cached_property
    singledispatchmethod = f.singledispatchmethod
elif version == (3, 9):
    cached_property = f.cached_property
    singledispatchmethod = f.singledispatchmethod
elif version == (3, 10):
    cached_property = f.cached_property
    singledispatchmethod = f.singledispatchmethod
elif version == (3, 11):
    cached_property = f.cached_property
    singledispatchmethod = f.singledispatchmethod
else:
    raise Exception('Current version not supported')
