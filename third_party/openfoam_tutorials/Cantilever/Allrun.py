#!/usr/bin/env python3
from foam import Foam


foam = Foam.from_file('case.yaml')
foam.save('case')
foam.cmd.all_run(overwrite=True, parallel=False)

path = next(log for log in foam.cmd.logs if foam.application in log.name)
with open(path.parent/'sigmaEq', 'w') as f:
    for line in path.read_text().splitlines():
        if 'sigmaEq' in line:
            f.write(line.strip().split()[3] + '\n')
