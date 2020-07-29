#=
Adapted from the original Python code on July 27, 2020

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

@author: Tarik Hoshan
=#

include("catmouse.jl")
using Plots

function plot_boundary(speed_ratio=4, angle_intervals=360)
    println("Getting boundary...")
    boundary = getBoundary(speed_ratio, angle_intervals)
    println("Plotting boundary in polar coordinates...")
    p = plot(boundary, proj=:polar, label="Boundary", 
                title="Escape Distance Boundary\nVelocity Ratio=$speed_ratio",
                linecolor=:blue)
    n = size(boundary[1])[1]
    alphas = boundary[1]
    distances = boundary[2]
    # Plot escape routes
    for i in 1:n
        if i % 10 == 0
            distance = distances[i]
            alpha = alphas[i]
            beta = maxDiffTimeCatMouse(distance, alpha, speed_ratio)[1]
            angles = [alpha, beta]
            rs = [distance, 1]
            plot!(p, angles, rs, proj=:polar, linecolor=:green, label=(i/10==floor(n/10) ? "Escape Paths" : ""))
        end
    end

    # Plot circle withon which the mouse can have a greater angular velocity than the cat.
    angles = [i * pi / 180 for i in 0:360]
    rs = [1 / speed_ratio for i in 0:360]
    plot!(p, angles, rs, proj=:polar, linecolor=:red, label="Rotation Boundary")

    display(p)
end

plot_boundary()
