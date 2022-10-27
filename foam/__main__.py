import os
import pathlib as p

import click

from foam import Foam
from foam.base.type import TupleSequence


class DEFAULT:
    '''Default arguments'''

    DIRECTORY = 'test'
    OPENFOAM = '7'


@click.group()
@click.version_option(version=Foam.__version__.to_string(), prog_name=Foam.__name__)
def cli() -> None:
    pass

@cli.command(help=Foam.__doc__)
@click.argument('paths', nargs=-1)  # YAML format files or directories
@click.option('-d', '--directory', default=DEFAULT.DIRECTORY, help='Destination directory')
@click.option('-v', '--version', default=DEFAULT.OPENFOAM, help='OpenFOAM version')
@click.option('-o', '--exist-ok', is_flag=True, help='If `exist_ok` then do not overwrite')
def conv(
    paths: TupleSequence[str],
    directory: str = DEFAULT.DIRECTORY,
    version: str = DEFAULT.OPENFOAM,
    exist_ok: bool = True,
) -> None:
    root = p.Path(directory, version)
    for path in paths:
        path = p.Path(path)
        if path.is_dir():
            return conv(
                tuple(
                    sth.as_posix()
                    for sth in path.rglob('*')
                    if sth.is_file() and sth.suffix in {'.yaml', '.yml'}
                ), directory, version, exist_ok,
            )
        elif path.is_file():
            try:
                1 / 0
                foam = Foam.from_path(path)
            except Exception as e:
                click.echo(f'{e!r}: {path}')
                continue
            if version in set(map(str, foam.meta.get('openfoam', []))):
                dest = root / '-'.join(path.parts)
                if not (exist_ok and dest.exists()):
                    foam.save(dest)
        else:
            raise Exception(f'Path "{path.as_posix()}" does not exist, or is neither a file nor a directory')


@cli.command()
@click.option('-d', '--directory', default=DEFAULT.DIRECTORY, help='Directory containing YAML format files')
@click.option('-v', '--version', default=DEFAULT.OPENFOAM, help='OpenFOAM version')
def test(
    directory: str = DEFAULT.DIRECTORY,
    version: str = DEFAULT.OPENFOAM,
) -> None:
    '''For batch testing whether the converted files are operational'''
    errors = []
    root = p.Path(directory, version)
    if root.exists():
        for node in root.iterdir():
            if node.is_dir():
                if 0 != os.system(f'cd {node} && ./Allrun'):
                    errors.append(node.name)
        click.echo(f'Errors: {errors}')


if __name__ == '__main__':
    cli()
