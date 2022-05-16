import json
import pathlib as p
import timeit

from foam import Foam


directories = {
    'tutorials/DNS',
    'tutorials/basic',
    'tutorials/incompressible',
}
number = 7

bench = {}
for directory in directories:
    for path in p.Path(directory).rglob('*.yaml'):
        path = path.as_posix()
        bench[path] = [[None, None] for _ in range(number)]
        foam = Foam.from_file(path)
        foam.save('case')
        for ith in range(number):
            for jth, func in enumerate([
                lambda: foam.cmd.raw('./Allrun'),
                lambda: foam.cmd.all_run(),
            ]):
                foam.cmd.all_clean()
                tic = timeit.default_timer()
                func()
                toc = timeit.default_timer()
                bench[path][ith][jth] = toc - tic
                print(path, toc-tic)
with open('bench.json', 'w') as f:
    json.dump(bench, f, ensure_ascii=False, indent=4)
