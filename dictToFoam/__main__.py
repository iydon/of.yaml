import argparse
import pathlib as p

from foam import Foam


parser = argparse.ArgumentParser(description=Foam.__doc__)
parser.add_argument('inputs', nargs='+', help='YAML format files')
parser.add_argument('-o', '--output', nargs='?', default='.', help='Destination directory')
parser.add_argument('--version', action='version', version=Foam.__version__)
args = parser.parse_args()

directory = p.Path(args.output)
for path in map(p.Path, args.inputs):
    Foam.from_file(path).save(directory/path.stem)
