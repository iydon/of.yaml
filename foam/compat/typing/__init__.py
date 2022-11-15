__all__ = ['Protocol']


import sys
import typing as t


version = (sys.version_info.major, sys.version_info.minor)
if version == (3, 7):
    from .v37 import Protocol
elif version == (3, 8):
    Protocol = t.Protocol
elif version == (3, 9):
    Protocol = t.Protocol
elif version == (3, 10):
    Protocol = t.Protocol
else:
    raise Exception('Current version not supported')
