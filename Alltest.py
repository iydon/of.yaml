#!/usr/bin/env poetry run python
import os
import pathlib as p

try:
    from dictToFoam import Foam
except:
    Foam = None


class test:
    root = p.Path(__file__).absolute().parent
    tutorials = root / 'tutorials'
    test = root / 'test'

    @classmethod
    def dict2foam(cls):
        for directory in cls.tutorials.glob('**/*'):
            if directory.is_dir():
                for path in directory.iterdir():
                    if path.suffix == '.yaml':
                        name = '_'.join(path.relative_to(cls.tutorials).parts)
                        dest = cls.test / name
                        if not dest.exists():
                            Foam.from_(path, dest=cls.test/name).save()

    @classmethod
    def alltest(cls):
        directories = []
        for directory in cls.test.iterdir():
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
    args = parser.parse_args()

    args.dict2foam and test.dict2foam()
    args.alltest and test.alltest()
