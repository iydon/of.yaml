__all__ = ['copytree']


import shutil
import sys


version = (sys.version_info.major, sys.version_info.minor)
if version == (3, 7):
    from .v37 import copytree
elif version in {(3, 8), (3, 9), (3, 10)}:
    copytree = shutil.copytree
else:
    raise Exception('Current version not supported')
