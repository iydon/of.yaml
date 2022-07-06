#!/usr/bin/env python3
import subprocess

from foam import Foam
from foam.app.command.adapter import Apps, AppByTimeI


assert subprocess.run('wmake', cwd='solvers/mySolver/', shell=True).returncode == 0
Apps['mySolver'] = AppByTimeI

foam = Foam.from_file('mixerVesselAMI2D.yaml')
foam.save('mixerVesselAMI2D')
foam.cmd.all_run(overwrite=True, parallel=True)
