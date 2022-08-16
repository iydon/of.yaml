#!/usr/bin/env python3
import subprocess

from foam import Foam
from foam.app.command.adapter import Apps, AppByTimeI


subprocess.run('wmake', cwd='new/pimpleDyMFoamTimed/')

Apps['pimpleDyMFoamTimed'] = AppByTimeI

foam = Foam.from_file('case.yaml')
foam.save('case')
foam.cmd.all_run(overwrite=False, parallel=True)
