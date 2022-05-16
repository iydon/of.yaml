import json
import pathlib as p
import timeit

from foam import Foam


repeat = 99
n_time = 999

bench = {}
for path in p.Path('tutorials').rglob('*.yaml'):
    path = path.as_posix()
    foam = Foam.from_file(path).save('case')
    control = foam['foam']['system', 'controlDict']
    if (
        foam.number_of_processors == 1 and
        '0' in foam['foam'] and
        control['startFrom'] == 'startTime' and
        control['stopAt'] == 'endTime'
    ):
        bench[path] = [[None, None] for _ in range(repeat)]
        control['endTime'] = n_time * float(control['deltaT'])
        for ith in range(repeat):
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
    json.dump(bench, f)
