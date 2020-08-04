#=
Adapted from the original Python code on July 27, 2020

Reference: Game of Cat and Mouse, https://www.youtube.com/watch?v=vF_-ob9vseM

The following functions assume a circle of radius 1, a cat velocity of 1 and
a mouse speed of 1 / CAT_TO_MOUSE_SPEED_RATIO.
The first two assumptions have no effect on the nature of the solution
as scaling the cirle up or down will just speed or slow things up. Same goes
for the cat speed. In fact, only the ratio of cat to mouse velocity has any
effect on the solution or lack of solution for that matter.

@author: Tarik Hoshan
=#

using Optim
DEBUG = false

#= Find angles for the two tangents to circle of radius 
r and center (0, 0) and passing by point x, y =#
function tangent_angles(r, x, y)
    if (r <= 0)
        throw(DomainError("Zero or negative radius."))
    end

    if x == r
        [0]
    elseif x == -r
        [π]
    elseif y == r
        [π/2]
    elseif y == -r
        [3*π/2]
    elseif x^2 + y^2 == r^2
        θ = atan(y/x)
        [θ]
    elseif x^2 + y^2 > r^2
        a = sqrt(-r^2+x^2+y^2)
        b = x + r
        θ1 = 2 * atan((y-a)/b)
        θ1 = θ1 > 0 ? θ1 : θ1 + 2 * π
        θ2 = 2 * atan((y+a)/b)
        θ2 = θ2 > 0 ? θ2 : θ2 + 2 * π
        [θ1, θ2]
    elseif x^2 + y^2 < r^2
        zeros(0)
    else
        throw(DomainError("Case not handled"))
    end
end

#=
alpha, distance: Polar coordinates of point M representing the mouse.
beta, 1: Polar coordinates of an arbitrary point P on the circle.
Return value: Distance between M and P
=#
function distanceToEdge(distance, alpha, beta)
    #=
    (cos(alpha), 0) represent the cartesian coordinates of M. We assume here
    that the mouse is located on the X axis.
    P is located at coordinates (cos(alpha), sin(alpha))
    =#
    return sqrt((distance - cos(alpha - beta)) ^ 2 + sin(alpha - beta) ^ 2)
end

#=
beta, 1: Coordinates of an arbitrary point P on the circle.
0, 1: Position of the cat. This assumption has no effect as we can always
use a rotation transform to position the cat at 0, 1.

We define here the distance of C to P as the length of the arc with the minimum
distance. Alternatively, the arc of lenth <= PI.
=#
function distanceViaEdge(beta)
    return min(abs(beta), 2 * pi - abs(beta))
end

#=
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
=#
function diffTimeCatMouse(distance, alpha, beta, speed_ratio)
    return distanceViaEdge(beta) - distanceToEdge(distance, alpha, beta) * speed_ratio
end

#=
alpha, distance: Polar coordinates of point M representing the mouse
0, 1: Position of the cat. This assumption has no effect as we can always
use a rotation transform to position the cat at 0, 1.

Determine the angle of point with polar coordinates (beta, 1) that maximizes
the difference in arrival time between the mouse and the cat. Note that the
shortest path from the mouse to the edge of the circle in not optimum.
=#
function maxDiffTimeCatMouse(distance, alpha, speed_ratio)
    #=
    We difference in time between the mouse arriving at point P and the cat
    arriving at point P is a piecewise function with two cases:
    - Case point P lies at an angle beta between 0 and PI in which case the 
      shortest path for the cat to reach P is beta.
    - Case point P lies at an angle beta between PI and 2 PI in which case
      the shortest path for the cat to reach P is 2 PI - beta.
    
    Accordingly the maximum of the piecewise function is the maximum of the
    maximums of both pieces. Note that since the optimize function provides
    the minimum, we minimize the negative of the function.
    =#
    f1(beta) = -(beta - speed_ratio * distanceToEdge(distance, alpha, beta))
    res = Optim.optimize(f1, 0.0, pi, abs_tol=1E-15)
    argmax1 = res.minimizer
    max1 = -res.minimum    
    
    f2(beta) = -((2 * pi - beta) - speed_ratio * distanceToEdge(distance, alpha, beta))
    res = Optim.optimize(f2, pi, 2*pi, abs_tol=1E-15)
    argmax2 = res.minimizer
    max2 = -res.minimum    
       
    if max1 >= max2
        return [argmax1, max1]
    else
        return [argmax2, max2]
    end
end

#=
alpha, distance: Polar coordinates of point M representing the mouse.
0, 1: Polar coordinates of cat
Given alpha, determine the minimum distance of the mouse from the center
to allow for an escape.
=#
function minimumEscapeDistance(alpha, speed_ratio)
    function f(distance)
        timediff = maxDiffTimeCatMouse(distance, alpha, speed_ratio)[2]
        timediff^2
    end

    distance = Optim.optimize(f, 0, 1).minimizer
    return distance
end

#=
Calculate a list of points defining a boundary between two regions. All the
points on top region represent success initial positions from which the mouse
has a guaranteed escape. The bottom region are failure start positions.
=#
function getBoundary(speed_ratio, angle_intervals)
    interval_size = pi * 2 / angle_intervals
    alphas = [i * interval_size for i in 0:angle_intervals]
    distances = [minimumEscapeDistance(alpha, speed_ratio) for alpha in alphas]
    if DEBUG
        for (i, alpha) in alphas
            distance=distances[i]
            println("$i $alpha $distance")
        end
    end
    return alphas, distances
end
    
