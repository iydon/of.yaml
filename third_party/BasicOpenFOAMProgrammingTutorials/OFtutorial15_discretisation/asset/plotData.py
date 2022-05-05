#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  6 11:04:35 2021

@author: artur
"""

import pathlib as p

import pandas as pd
import matplotlib
import matplotlib.pyplot as plt


root = p.Path(__file__).parent
case = root.parent / 'case'
font = {'family' : 'serif',
        'weight' : 'normal',
        'size'   : 16}

matplotlib.rc('font', **font)

# %% Read the data.
refData = {path.stem.split("_")[1]: pd.read_csv(path)
           for path in (root/"refData").iterdir()}
currentData = None
try:
    currentData = pd.read_csv(case/"postProcessing/samplingLine/0.5/centrelineData_T.csv")
except FileNotFoundError:
    pass

# %% Plot solutions obtained using each scheme.
fig, ax = plt.subplots(1, figsize=(8, 6))
ax.set_xlabel("x [m]")
ax.set_ylabel(r"$\phi$ [-]")
ax.set_ylim((-0.05, 1.05))
for s in refData:
    ax.plot(refData[s]["x"], refData[s]["T"], "o--", lw=1, ms=6, mew=0, label=s)
if currentData is not None:
    ax.plot(currentData["x"], currentData["T"], "rs--", lw=1, ms=6, mew=0, label="Custom scheme")
xlim = ax.get_xlim()
ax.hlines([0, 1], xlim[0], xlim[1], color="k", ls="--", alpha=0.5, zorder=-10)
ax.set_xlim(xlim)
ax.legend(loc="lower left", framealpha=1)
plt.tight_layout()
plt.savefig("cellCentreValues.png", dpi=200, bbox_inches="tight")

plt.show()
