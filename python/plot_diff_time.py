#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 16:18:35 2019

Surface plot of the difference of arrival time to the edge between the cat and
the mouse starting from a given distance " on the X axis for the mouse and
an angle beta for the cat.

Positive values represent initial conditions that allow a mouse escape with a
difference of time represented by the z axis.

Zero or negative values indicate a failure to escape via a straight line
starting from these initial conditions.


@author: tarik
"""

import math
import catmouse
import numpy as np

# This import registers the 3D projection, but is otherwise unused.
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import

import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter

# Prepare meshgrid
X = np.arange(0, 1, 0.025)
Y = np.arange(0, 2 * math.pi, 0.025)
X, Y = np.meshgrid(X, Y)

# Function to strip off alpha and get optimal distance only
def f(distance, beta):
    return catmouse.maxDiffTimeCatMouse(distance, beta)[1]

# Calculate distance difference. Positive means safe zone
Z = np.vectorize(f)(X, Y)

# Create a 3D surface plot
fig = plt.figure()
ax = fig.gca(projection='3d')

# Plot the surface.
surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm, linewidth=0, antialiased=False)

# Customize the z axis.
ax.set_zlim(-7, 7)
ax.zaxis.set_major_locator(LinearLocator(10))
ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

# Add a color bar which maps values to colors.
fig.colorbar(surf, shrink=0.5, aspect=5)

plt.show()
