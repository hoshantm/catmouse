#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 12:08:09 2019

Reference: Game of Cat and Mouse, https://www.youtube.com/watch?v=vF_-ob9vseM

The following functions assume a circle of radius 1, a cat velocity of 1 and
a mouse speed of 1 / CAT_TO_MOUSE_SPEED_RATIO.
The first two assumptions have no effect on the nature of the solution
as scaling the cirle up or down will just speed or slow things up. Same goes
for the cat speed. In fact, only the ratio of cat to mouse velocity has any
effect on the solution or lack of solution for that matter.

@author: tarik
"""

import math
import numpy as np
from scipy.optimize import minimize
from scipy.optimize import brentq

CAT_TO_MOUSE_SPEED_RATIO = 4
ANGLE_INTERVALS = 360

'''
distance: distance of the mouse from the center.

alpha: Angle between a line originating from the center and a line orinating
from the center of the circle and passing through the point M representing 
the mouse. The first line determines a point P through which it itersects
with the circle. We assume here that M is located on the X axis. This
assumption does not affect anything as we can rotate the entire world to 
align the mouse with the X axis.

Given the above two parameters, calculates the distance between points M and P 
'''
def distanceToEdge(distance, alpha):
    '''
    (cos(alpha), 0) represent the cartesian coordinates of M. We assume here
    that the mouse is located on the X axis.
    P is located at coordinates (cos(alpha), sin(alpha))
    '''
    return math.sqrt((distance - math.cos(alpha)) ** 2 + math.sin(alpha) ** 2)

'''
alpha: Angle between a line originating from the center and a line orinating
from the center of the circle and passing through the point M representing 
the mouse. The first line determines a point P through which it itersects
with the circle. We assume here that M is located on the X axis. This
assumption does not affect anything as we can rotate the entire world to 
align the mouse with the X axis.

beta: Angle between a line originating from the center and intersecting the
circle at point C representing the cat, and the X axis.

Both alpha and beta are measured in radian clockwise from the X axis. That
makes it trivial to measure the arc lengths between C and P. The word "lengths"
is plural as we can calculate the lengths of both arcs determined by C and P.

We define here the distance of C to M as the length of the arc with the minimum
distance. Alternatively, the arc of lenth <= PI.
'''
def distanceViaEdge(alpha, beta):
    return min(abs(beta - alpha), 2 * math.pi - abs(beta - alpha))

'''
Given distance, alpha and beta (see definitions above), calculate the difference
in time between the mouse arrival at point P determined by angle alpha and
the arrival of the cat to pint P from point C. Note that since the cat is
CAT_TO_MOUSE_SPEED_RATIO faster than the mouse, it takes the mouse time is
multiplied by CAT_TO_MOUSE_SPEED_RATIO. Alternatively, we could have divided
the cat time by CAT_TO_MOUSE_SPEED_RATIO. Since the cat velocity is assumed
to be one, we do not bother dividing by one to get the time.
The idea of this function is to find out if a mouse at a given location
can escape via a point P determined by alpha. A positive time difference
indicates a success. Conversly, a zero or negative time difference determines
a failure. 
'''
def diffTimeCatMouse(distance, alpha, beta):
    return distanceViaEdge(alpha, beta) - distanceToEdge(distance, alpha) * CAT_TO_MOUSE_SPEED_RATIO

'''
Given a distance (mouse location on the X axis. See previous definitions) and
angle beta determining the cat location (see previous definitions) calculate
alpha that will maximize the arrival time difference at point P determined
by alpha, and the arrival of the cat to point P.
A positive number indicates that the initial conditions of distance and beta
guarantees the mouse escaping in a straight line via point P.
What is couterintuitive here is that the mouse could swim along a line not
necessary aligned with the X axis and shave off some time.
'''
def maxDiffTimeCatMouse(distance, beta):
    f1 = lambda alpha : alpha - beta + CAT_TO_MOUSE_SPEED_RATIO * math.sqrt((distance - math.cos(alpha)) ** 2 + math.sin(alpha) ** 2)
    x0 = np.array([beta - math.pi / 2])
    bounds = [(beta - math.pi, beta)]
    res = minimize(f1, x0, method='L-BFGS-B', bounds=bounds)
    argmax1 = res['x'][0]
    if argmax1 < 0:
        argmax1 = math.pi * 2 + argmax1
    max1 = -res['fun'][0]    
    
    f2 = lambda alpha : -alpha + beta - 2 * math.pi + CAT_TO_MOUSE_SPEED_RATIO * math.sqrt((distance - math.cos(alpha)) ** 2 + math.sin(alpha) ** 2)
    x0 = np.array([0])
    bounds = [(beta - 2 * math.pi, beta - math.pi)]
    res = minimize(f2, x0, method='L-BFGS-B', bounds=bounds)
    argmax2 = res['x'][0]
    if argmax2 < 0:
        argmax2 = math.pi * 2 + argmax2
    max2 = -res['fun'][0]    
       
    if max1 >= max2:
        return argmax1, max1
    else:
        return argmax2, max2

'''
Given a given angle beta as previously defined, calculate the minimum distance
from the center to ensure the mouse escape. Meaning that the smaller the angle,
the closer the mouse should be to the edge.
'''
def minimumEscapeDistance(beta):
    f = lambda distance : maxDiffTimeCatMouse(distance, beta)[1]
    x = brentq(f, 0, 1)
    return x

'''
Calculate a list of points defining a boundary between two regions. All the
points on top region represent success initial positions from which the mouse
has a guaranteed escape. The bottom region are failure start positions.
'''
def getBoundary():
    interval_size = math.pi * 2 / ANGLE_INTERVALS
    betas = [i * interval_size for i in range(ANGLE_INTERVALS + 1)]
    distances = [minimumEscapeDistance(beta) for beta in betas]
    return betas, distances
