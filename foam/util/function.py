__all__ = ['grammar', 'license']


import pathlib as p


root = p.Path(__file__).parents[1]


def grammar() -> str:
    return (root/'static'/'grammar'/'openfoam.lark').read_text()


def license(full_text: bool = False) -> str:
    if full_text:
        return (root/'static'/'LICENSE.txt').read_text()
    else:
        return 'GPL-3.0-only'
