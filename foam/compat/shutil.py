__all__ = ['copytree']


import shutil
import sys


def copytree(
    src, dst,
    symlinks=False, ignore=None, copy_function=shutil.copy2,
    ignore_dangling_symlinks=False, dirs_exist_ok=False,
):
    kwargs = {
        'symlinks': symlinks, 'ignore': ignore, 'copy_function': copy_function,
        'ignore_dangling_symlinks': ignore_dangling_symlinks,
    }
    if sys.version_info >= (3, 8):
        kwargs['dirs_exist_ok'] = dirs_exist_ok
    return shutil.copytree(src, dst, **kwargs)
