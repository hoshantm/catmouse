#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 21:00:51 2019

Plot the boundary line separating two regions. All the
points on top region represent success initial positions from which the mouse
has a guaranteed escape. The bottom region are failure start positions.

The area below the red line are positions that can be reached by the mouse 
starting from the center and following a spiraling path. The optimal
path is calculated by spyral_path.py

The intersection between the upper success region and the region below the
red line represent a set of initial positions that are reachable by maneuvering
from the center, and guaranteing an escape route through a straight line.
The point of escape can be found using catmouse.maxDiffTimeCatMouse function.

@author: tarik
"""

from catmouse import CAT_TO_MOUSE_SPEED_RATIO
from catmouse import getBoundary

import matplotlib.pyplot as plt
import math

betas, distances = getBoundary()

plt.scatter(betas, distances, s=1)

plt.plot([0, 2 * math.pi],
                [1/CAT_TO_MOUSE_SPEED_RATIO,
                 1/CAT_TO_MOUSE_SPEED_RATIO], 'r-')

plt.xlim(0, 2 * math.pi)
plt.ylim(0, 1)
plt.xlabel('angle of cat with X axis in radian')
plt.ylabel('distance from center')
plt.title = 'Escape region boundary plot'

plt.show()
