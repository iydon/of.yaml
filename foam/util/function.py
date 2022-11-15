__all__ = ['dict_without_keys', 'dry_run', 'grammar', 'license']


import pathlib as p
import subprocess


root = p.Path(__file__).parents[1]


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
