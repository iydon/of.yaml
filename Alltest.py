#!/usr/bin/env poetry run python
import os
import pathlib as p
import typing as t

try:
    from dictToFoam import Foam
except:
    Foam = None


class test:
    root = p.Path(__file__).absolute().parent
    tutorials = root / 'tutorials'
    test = root / 'test'

    @classmethod
    def dict2foam(cls, version: t.Union[str, int]):
        assert Foam is not None
        for directory in cls.tutorials.glob('**/*'):
            if directory.is_dir():
                for path in directory.iterdir():
                    if path.suffix == '.yaml':
                        name = '_'.join(path.relative_to(cls.tutorials).parts)
                        dest = cls.test / str(version) / name
                        if not dest.exists():
                            foam = Foam.from_file(path)
                            if str(foam.meta.get('openfoam', '')) == str(version):
                                foam.save(dest)

    @classmethod
    def alltest(cls, version: t.Union[str, int]):
        directories = []
        for directory in (cls.test/str(version)).iterdir():
            if directory.is_dir():
                ret = os.system(f'cd {directory} && ./Allrun')
                if ret != 0:
                    directories.append(directory)
                    print('Error:', directory.name)
        print('Errors:', directories)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--dict2foam', action='store_true')
    parser.add_argument('--alltest', action='store_true')
    parser.add_argument('--version', action='store', type=str, help='OpenFOAM version')
    args = parser.parse_args()

    version = args.version or 7
    args.dict2foam and test.dict2foam(version)
    args.alltest and test.alltest(version)
