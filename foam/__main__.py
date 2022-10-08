import os
import pathlib as p
import typing as t

import click

from foam import Foam


class DEFAULT:
    CONV_DIRECTORY = '.'
    TEST_DIRECTORY = 'test'
    OPENFOAM = '7'


@click.group()
@click.version_option(version=Foam.__version__.to_string(), prog_name=Foam.__name__)
def cli():
    pass

@cli.command(help=Foam.__doc__)
@click.argument('paths', nargs=-1)  # YAML format files or directories
@click.option('-d', '--directory', default=DEFAULT.CONV_DIRECTORY, help='Destination directory')
@click.option('-v', '--version', default=None, help='OpenFOAM version')
@click.option('-o', '--exist-ok', is_flag=True, help='If `exist_ok` then do not overwrite')
def conv(paths: t.Tuple[str, ...], directory: str, version: str, exist_ok: bool) -> None:
    root = p.Path(directory) if version is None else p.Path(directory, version)
    for path in map(p.Path, paths):
        if path.exists():
            if path.is_file():
                dest = root / path.stem
                if not (exist_ok and dest.exists()):
                    foam = Foam.from_file(path)
                    if version is None or version in set(map(str, foam.meta.get('openfoam', []))):
                        foam.save(dest)
            elif path.is_dir():
                path = path.absolute()
                for sth in path.glob('**/*'):
                    if sth.is_file():
                        try:
                            foam = Foam.from_file(sth)
                        except Exception:  # TODO: Foam.from_file exception
                            continue
                        if version is None or version in set(map(str, foam.meta.get('openfoam', []))):
                            name = '_'.join(sth.relative_to(path).parts)
                            dest = root / name
                            if not (exist_ok and dest.exists()):
                                foam.save(dest)

@cli.command()
@click.option('-d', '--directory', default=DEFAULT.TEST_DIRECTORY, help='Directory containing YAML format files')
@click.option('-v', '--version', default=DEFAULT.OPENFOAM, help='OpenFOAM version')
def test(directory: str, version: str) -> None:
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
