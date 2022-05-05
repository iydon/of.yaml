#!/bin/bash

# ===
# Script for automatically compiling, running and testing all of the tutorials.
# ===

# run a command and redirect outputs to /dev/null, only print PASS or FAIL
# depending on whether errors occured or not
run () {
    # run the command and get rid of the outputs
    $@ >/dev/null 2>&1
    # check return code, 0 indicates success
    if [ $? -eq 0 ]; then
        echo "    PASS: "$@
    else
        echo "    FAIL: "$@
    fi
}

# go over all tutorial directories
for tutorialDir in */ ; do
    if [[ $tutorialDir = *OFtutorial* ]]; then
        echo "Checking:" $tutorialDir

        # navigate to the tutorial
        cd $tutorialDir

        # python script
        cat > test.py << EOF
import pathlib as p
import sys

from foam import Foam


root = p.Path('.').absolute().parents[2]
sys.path.append(root.as_posix())

foam = Foam \
    .from_file('case.yaml') \
    .save('case')
codes = foam.cmd.all_run()

assert all(code == 0 for code in codes)
EOF

        # test building and running
        run ./Allwmake
        run python test.py

        # go back to main directory
        cd ..
    fi
done
