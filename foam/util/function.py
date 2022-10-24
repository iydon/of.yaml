__all__ = ['dict_without_keys', 'grammar', 'license']


import pathlib as p


root = p.Path(__file__).parents[1]


def dict_without_keys(data: dict, *keys: str) -> dict:
    # dict := t.Dict[t.Hashable, t.Any]
    return {key: data[key] for key in data.keys() ^ keys}


def grammar() -> str:
    return (root/'static'/'grammar'/'openfoam.lark').read_text()


def license(full_text: bool = False) -> str:
    if full_text:
        return (root/'static'/'LICENSE.txt').read_text()
    else:
        return 'GPL-3.0-only'
