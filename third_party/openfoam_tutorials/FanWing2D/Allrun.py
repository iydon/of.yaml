#!/usr/bin/env python3
from foam import Foam
from foam.app.command.adapter import Apps, AppByTimeI


Apps['pimpleDyMFoam'] = AppByTimeI

foam = Foam.from_file('case.yaml')
foam.save('case')
foam.cmd.all_run(overwrite=True, parallel=False)
