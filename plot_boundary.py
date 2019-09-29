#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 21:00:51 2019

Plot the boundary line separating two regions. All the points in the inner
region represent success initial positions from which the mouse has a
guaranteed escape through a straight line. The outer points  in the outer
region are failure start positions.

The points within the red circle are positions that can be reached by the
mouse starting from the center and following a spiraling path. The optimal
path is calculated by spyral_path.py

The intersection between the outer region and the red circle represents the set
of points that have an escape route through a straight line and are reachable
from the center.

@author: tarik
"""

import catmouse

import matplotlib.pyplot as plt
import math

catmouse.CAT_TO_MOUSE_SPEED_RATIO = 4
alphas, distances = catmouse.getBoundary()

ax = plt.subplot(111, projection='polar')

# Plot escape boundary
ax.plot(alphas, distances)

# Plot escape routes
for i, (alpha, distance) in enumerate(zip(alphas, distances)):
    if i % 10 == 0:
        beta = catmouse.maxDiffTimeCatMouse(distance, alpha)[0]
        angles = [alpha, beta]
        rs = [distance, 1]
        ax.plot(angles, rs, 'g')

# Plot circle withon which the mouse can have a greater angular velocity than the cat.

angles = [i * math.pi / 180 for i in range(361)]
rs = [1 / catmouse.CAT_TO_MOUSE_SPEED_RATIO for i in range(361)]
ax.plot(angles, rs, 'r')

ax.set_rmin(0)
ax.set_rmax(1)
ax.set_rticks([0.25, 0.5, 0.75, 1])  # less radial ticks
ax.set_rlabel_position(-22.5)  # get radial labels away from plotted line
ax.grid(True)

ax.set_title('Escape region boundary plot', va='bottom')
plt.show()
