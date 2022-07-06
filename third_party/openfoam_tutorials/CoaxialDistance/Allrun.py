#!/usr/bin/env python3
from foam import Foam


foam = Foam.from_file('case.yaml')
foam.save('case')
foam.cmd.all_run(overwrite=True, parallel=True)
