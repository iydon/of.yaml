__all__ = ['license']


import pathlib as p


root = p.Path(__file__).parents[1]


def license(full_text: bool = False) -> str:
    if full_text:
        return (root/'static'/'LICENSE.txt').read_text()
    else:
        return 'GPL-3.0-only'
