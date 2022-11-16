__all__ = ['deprecated_classmethod', 'dict_without_keys', 'dry_run', 'grammar', 'license']


import pathlib as p
import subprocess
import typing as t

from .decorator import message


root = p.Path(__file__).parents[1]


def deprecated_classmethod(cls_meth: classmethod, old: t.Optional[str] = None) -> classmethod:
    func = cls_meth.__func__
    new = func.__name__
    if old is None:
        replace = lambda char: f'_{char.lower()}' if char.isupper() else char
        old = ''.join(map(replace, new)).lstrip('_')
    msg = f'I am using camelCase to distinguish between class methods and instance methods, so please use `{new}` instead of `{old}`'
    return classmethod(message(msg)(func))


def dict_without_keys(data: dict, *keys: str) -> dict:
    # dict := t.Dict[t.Hashable, t.Any]
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
