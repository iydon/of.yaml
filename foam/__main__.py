__all__ = ['cnv', 'run']


import pathlib as p
import subprocess
import typing as t

import click

from foam import Foam
from foam.base.lib import tqdm
from foam.base.type import Any, TupleSeq


class DEFAULT:
    '''Default arguments'''

    DIRECTORY = 'test'
    OPENFOAM = '7'


def _cnv(src: p.Path, dst: p.Path, version: str, exist_ok: bool) -> bool:
    try:
        foam = Foam.fromPath(src)
    except Exception as e:
        click.echo(f'{e!r}: {src}')
        return False
    else:
        if version in set(map(str, foam.meta.get('openfoam', []))):
            path = dst / '-'.join(src.parts)
            if exist_ok or not path.exists():
                foam.save(path)
        return True


def _run(directory: p.Path) -> bool:
    cp = subprocess.run('./Allrun', capture_output=True, cwd=directory, shell=True)
    return cp.returncode == 0


@click.group()
@click.version_option(version=Foam.__version__.to_string(), prog_name=Foam.__name__)
def cli() -> None:
    pass


@cli.command(help=Foam.__doc__)
@click.argument('paths', nargs=-1)  # YAML format files or directories
@click.option('-d', '--directory', default=DEFAULT.DIRECTORY, help='Destination directory')
@click.option('-v', '--version', default=DEFAULT.OPENFOAM, help='OpenFOAM version')
@click.option('-o', '--exist-ok', is_flag=True, help='If `exist_ok` then do not overwrite')
def cnv(paths: TupleSeq[str], directory: str = DEFAULT.DIRECTORY, version: str = DEFAULT.OPENFOAM, exist_ok: bool = True) -> None:
    dst = p.Path(directory, version)
    for path in paths:
        src = p.Path(path)
        if src.is_dir():
            for path in src.rglob('*'):
                if path.is_file() and path.suffix in {'.yaml', '.yml'}:
                    assert _cnv(path, dst, version, exist_ok), path
        elif src.is_file():
            assert _cnv(src, dst, version, exist_ok), src
        else:
            raise Exception(f'Path "{src.as_posix()}" does not exist, or is neither a file nor a directory')


@cli.command()
@click.option('-d', '--directory', default=DEFAULT.DIRECTORY, help='Directory containing YAML format files')
@click.option('-v', '--version', default=DEFAULT.OPENFOAM, help='OpenFOAM version')
def run(
    directory: str = DEFAULT.DIRECTORY,
    version: str = DEFAULT.OPENFOAM,
) -> None:
    '''For batch testing whether the converted files are operational'''
    pbar: t.Callable[[t.Iterator[p.Path]], t.Iterable[p.Path]] \
        = tqdm.tqdm if tqdm.is_available() else lambda x: x
    dst = p.Path(directory, version)
    for path in pbar(dst.iterdir()):
        if path.is_dir():
            assert _run(path), path


if __name__ == '__main__':
    cli()
