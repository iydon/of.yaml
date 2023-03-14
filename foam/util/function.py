__all__ = ['deprecated_classmethod', 'dict_without_keys', 'dry_run', 'grammar', 'license']


import subprocess
import typing as t

from .decorator import message
from ..base.config import root
from ..base.type import DictAny2, Func1


def deprecated_classmethod(method: classmethod, old: t.Optional[str] = None) -> classmethod:
    func = method.__func__
    new = func.__name__
    if old is None:
        replace: Func1[str, str] \
            = lambda char: f'_{char.lower()}' if char.isupper() else char
        old = ''.join(map(replace, new)).lstrip('_')
    msg = f'I am using camelCase to distinguish between class methods and instance methods, so please use `{new}` instead of `{old}`'
    return classmethod(message(msg)(func))


def dict_without_keys(data: DictAny2, *keys: str) -> dict:
    return {key: data[key] for key in data.keys() ^ keys}


def dry_run(recover: bool = False) -> None:
    from ..util.object.popen import Origin, DryRun

    subprocess.Popen = Origin if recover else DryRun


def grammar() -> str:
    return (root/'static'/'grammar'/'openfoam.lark').read_text()


def license(full_text: bool = False) -> str:
    if full_text:
        return (root/'static'/'LICENSE.txt').read_text()
    else:
        return 'GPL-3.0-only'
