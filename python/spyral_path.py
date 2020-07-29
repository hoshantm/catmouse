#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 05:00:46 2019

Plot of the spiral path representing the optimal route towards the edge of the
circle while staying diametrically opposite to the cat position. The assumed
initial positions are center for the mouse and angle PI for the cat. The mouse
original velocity vector is 1 / CAT_TO_MOUSE_SPEED_RATIO along the positive
direction of the X axis. We also assume that the cat moves clockwise along the
edge of the circle at constant velocity 1. The mouse progress towards the edge
will progressively slow down as it needs to circle faster and faster around the
center, until it reaches a radius equal to 1 / CAT_TO_MOUSE_SPEED_RATIO,
assuming a radius of 1. All of the assumptions above do not have any effect
on the nature of the solution. Scaling and rotation can fix that. A change of
cat direction would require the mouse to change its rotation direction
instantly and follow a mirror image of the remainder of the escape path
in relation with the radius passing by the current mouse location.

The path is the solution of the following diffential equation:
sqrt(r'^2 + r^2) = 1/4
r' = sqrt(1/16 - r^2)
Using https://www.symbolab.com ODE solver, we get:
r(t) = sin(t + c1) / 4
c1 represents the original time, but also the angle theta since the angle
velocity is constant and equal to one radian per second. We set c1 to zero.
Notes:
- For a CAT_TO_MOUSE_SPEED_RATIO different than 4, use
  1/CAT_TO_MOUSE_SPEED_RATIO instead of 1/4 and 1/CAT_TO_MOUSE_SPEED_RATIO^2
  instead of 1/16.
- With CAT_TO_MOUSE_SPEED_RATIO = 4, past t=PI/2, the mouse will start
  spiraling back towards the center. It's up to us human to determine the
  boundaries of the mathematical solution.
- When transformed from polar to cartesian coordinates, it seems that the
  path is simply a half circle of radius 1/4 and center (0, 1/8). I did
  not verify this though.

@author: tarik
"""

import math
import matplotlib.pyplot as plt

INTERVALS = 1000
inc = math.pi / 2 / INTERVALS
thetas = [i * inc for i in range(INTERVALS + 1)]
rs = [math.sin(theta) / 4 for theta in thetas]

ax = plt.subplot(111, projection='polar')
ax.plot(thetas, rs)

# draw circle
thetas2 = [2 * math.pi / INTERVALS * i for i in range(INTERVALS+1)]
rs2 = [1.0 / 4.0 for i in range(INTERVALS+1)]
ax.plot(thetas2, rs2)

ax.set_rmax(1)
ax.set_rticks([0.25, 0.5, 0.75, 1])  # less radial ticks
ax.set_rlabel_position(-22.5)  # get radial labels away from plotted line
ax.grid(True)

plt.show()

'''
Verify that the velocity is constant = 1/4 regardless of the
time between 0 and PI/2. The value of frac can be modified
to any value between 0 and 1, speed should always round up
to 0.25
'''
frac = 0.3
t = math.pi / 2 * frac
theta1 = t
r1 = math.sin(theta1) / 4

epsilon = 0.00001
theta2 = t + epsilon
r2 = math.sin(theta2) / 4

x1 = math.cos(theta1) * r1
y1 = math.sin(theta1) * r1

x2 = math.cos(theta2) * r2
y2 = math.sin(theta2) * r2

speed = math.sqrt((x2 - x1)**2 + (y2 - y1)**2) / epsilon
speed = round(speed, 10)
print(speed)
