#!/usr/bin/env python3
import subprocess
import typing as t

from foam import Foam


def line2dict(line: str) -> t.Dict[str, float]:
    floats = [
        float(x.replace(")", "").replace("(", ""))
        for x in line.split()
    ]
    return {
        'time': floats[0],
        'force': {
            'pressure': floats[1:4],
            'viscous': floats[4:7],
            'porous': floats[7:10],
        },
        'moment': {
            'pressure': floats[10:13],
            'viscous': floats[13:16],
            'porous': floats[16:19],
        },
    }


foam = Foam.from_file('case.yaml')
foam.save('case')
foam.cmd.all_run(overwrite=True, parallel=False)

times, lifts, drags, moments = [], [], [], []
with open('case/postProcessing/airfoil/0/forces.dat', 'r') as f:
    for line in f:
        if line[0] == '#':
            continue
        data = line2dict(line)
        times.append(data['time'])
        lifts.append(data['force']['pressure'][1]+data['force']['viscous'][1])
        drags.append(data['force']['pressure'][0]+data['force']['viscous'][0])
        moments.append(data['moment']['pressure'][2]+data['moment']['viscous'][2])
with open('forces.txt', 'w') as f:
    for time, lift, drag, moment in zip(times, lifts, drags, moments):
        f.write(f'{time} {lift} {drag} {moment}\n')
subprocess.run('./gnuplot_script.sh')
