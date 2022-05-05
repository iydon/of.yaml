#!/bin/bash

# ===
# Script for cleaning all of the tutorials.
# ===

for tutorialDir in */ ; do
    if [[ $tutorialDir = *OFtutorial* ]]; then
        echo "Cleaning:" $tutorialDir

        cd $tutorialDir
        ./Allwclean
        rm -rf case/ test.py
        cd ..
    fi
done
