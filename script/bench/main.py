import json
import os
import pathlib as p
import typing as t

from foam.namespace.full import Foam, Timer


def is_valid(foam: Foam, threshold: t.Optional[int] = None) -> bool:
    threshold = threshold or os.cpu_count()
    if foam.number_of_processors == 1:
        return True
    elif foam.number_of_processors > threshold:
        return False
    else:
        for static in foam['static']:
            if static['name'] == 'Allrun':
                break
        else:
            return False
        return 'runParallel' in static['data']


repeat = 7
n_time = 19

bench = {}
timer = Timer.default()
root = p.Path('extra', 'tutorial', 'tutorials', os.environ['WM_PROJECT_VERSION'])
for path in root.rglob('*.yaml'):
    foam = Foam.fromPath(path).save(f'case/{path.stem}')
    control = foam['foam']['system', 'controlDict']
    if control['startFrom']=='startTime' and control['stopAt']=='endTime' and is_valid(foam, 4):
        key = path.as_posix()
        bench[key] = [[None, None] for _ in range(repeat)]
        control['endTime'] = float(control['startTime']) + n_time*float(control['deltaT'])
        for ith in range(repeat):
            for jth, func in enumerate([
                lambda: foam.cmd.raw('./Allrun'),
                lambda: foam.cmd.all_run(),
            ]):
                foam.cmd.all_clean()
                with timer.tic_toc(key, ith, jth) as t:
                    func()
                bench[key][ith][jth] = float(t)
                print(path, float(t))
with open('bench.json', 'w') as f:
    json.dump(bench, f)
