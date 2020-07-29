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
DEBUG = False

'''
alpha, distance: Polar coordinates of point M representing the mouse.
beta, 1: Polar coordinates of an arbitrary point P on the circle.
Return value: Distance between M and P
'''
def distanceToEdge(distance, alpha, beta):
    '''
    (cos(alpha), 0) represent the cartesian coordinates of M. We assume here
    that the mouse is located on the X axis.
    P is located at coordinates (cos(alpha), sin(alpha))
    '''
    return math.sqrt((distance - math.cos(alpha - beta)) ** 2 + math.sin(alpha - beta) ** 2)

'''
beta, 1: Coordinates of an arbitrary point P on the circle.
0, 1: Position of the cat. This assumption has no effect as we can always
use a rotation transform to position the cat at 0, 1.

We define here the distance of C to P as the length of the arc with the minimum
distance. Alternatively, the arc of lenth <= PI.
'''
def distanceViaEdge(beta):
    return min(abs(beta), 2 * math.pi - abs(beta))

'''
alpha, distance: Polar coordinates of point M representing the mouse.
beta, 1: Polar coordinates of an arbitrary point P on the circle.
Return: Difference in time between the cat arrival at point P traveling on
the edge of the circle and the arrival of the mouse at point P traveling through
a straight line from point M.
Cat velocity: 1
Mouse velocity: 1 / CAT_TO_MOUSE_SPEED_RATIO

Since the cat velocity is assumed to be one, we do not bother dividing by one to
get the cat travel time.

The idea of this function is to find out if a mouse at a given location
can escape via a point P determined by alpha. A positive time difference
indicates a success. Conversly, a zero or negative time difference determines
a failure. 
'''
def diffTimeCatMouse(distance, alpha, beta):
    return distanceViaEdge(beta) - distanceToEdge(distance, alpha, beta) * CAT_TO_MOUSE_SPEED_RATIO

'''
alpha, distance: Polar coordinates of point M representing the mouse
0, 1: Position of the cat. This assumption has no effect as we can always
use a rotation transform to position the cat at 0, 1.

Determine the angle of point with polar coordinates (beta, 1) that maximizes
the difference in arrival time between the mouse and the cat. Note that the
shortest path from the mouse to the edge of the circle in not optimum.
'''
def maxDiffTimeCatMouse(distance, alpha):
    f1 = lambda beta : -(beta - CAT_TO_MOUSE_SPEED_RATIO * distanceToEdge(distance, alpha, beta))
    x0 = np.array([0])
    bounds = [(0, math.pi)]
    res = minimize(f1, x0, method='L-BFGS-B', bounds=bounds)
    argmax1 = res['x'][0]
    max1 = -res['fun'][0]    
    
    f2 = lambda beta : -((2 * math.pi - beta) - CAT_TO_MOUSE_SPEED_RATIO * distanceToEdge(distance, alpha, beta))
    x0 = np.array([2 * math.pi])
    bounds = [(math.pi, 2 * math.pi)]
    res = minimize(f2, x0, method='L-BFGS-B', bounds=bounds)
    argmax2 = res['x'][0]
    max2 = -res['fun'][0]    
       
    if max1 >= max2:
        return argmax1, max1
    else:
        return argmax2, max2

'''
alpha, distance: Polar coordinates of point M representing the mouse.
0, 1: Polar coordinates of cat
Given alpha, determine the minimum distance of the mouse from the center
to allow for an escape.
'''
def minimumEscapeDistance(alpha):
    f = lambda distance : maxDiffTimeCatMouse(distance, alpha)[1]
    distance = brentq(f, 0, 1)
    return distance

'''
Calculate a list of points defining a boundary between two regions. All the
points on top region represent success initial positions from which the mouse
has a guaranteed escape. The bottom region are failure start positions.
'''
def getBoundary():
    interval_size = math.pi * 2 / ANGLE_INTERVALS
    alphas = [i * interval_size for i in range(ANGLE_INTERVALS + 1)]
    distances = [minimumEscapeDistance(alpha) for alpha in alphas]
    if DEBUG:
        for i, alpha in enumerate(alphas):
            print (i, alpha, distances[i])
    return alphas, distances
