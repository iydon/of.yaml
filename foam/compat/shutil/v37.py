__all__ = ['copytree']


import shutil
import sys


def copytree(
    src, dst,
    symlinks=False, ignore=None, copy_function=shutil.copy2,
    ignore_dangling_symlinks=False, dirs_exist_ok=False,
):
    try:
        return shutil.copytree(
            src, dst,
            symlinks=symlinks, ignore=ignore, copy_function=copy_function,
            ignore_dangling_symlinks=ignore_dangling_symlinks,
        )
    except FileExistsError as e:
        if not dirs_exist_ok:
            raise e
