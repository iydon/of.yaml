__all__ = ['cached_property', 'singledispatchmethod']


import functools as f
import sys


version = (sys.version_info.major, sys.version_info.minor)
if version == (3, 7):
    from .v37 import cached_property, singledispatchmethod
elif version in {(3, 8), (3, 9), (3, 10)}:
    cached_property = f.cached_property
    singledispatchmethod = f.singledispatchmethod
else:
    raise Exception('Current version not supported')
