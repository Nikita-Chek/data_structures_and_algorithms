
import Statistics: mean
using Plots

function ginicoefficient(x::AbstractArray)
    n = length(x)
    m = sum(x) / n
    return sum(j -> sum(i -> abs(x[i] - x[j]), 1:n),  1:n) / (2 * n^2 * m)
end

function lorenz_curve(x::AbstractArray)
    s = sum(x)
    n = length(x)
    p = map(i -> sum(x[1:i]) / s, 1:n)
    plot!([0,1], [0,1], label = "equality line")
    plot!(1/n:1/n:1, p, title = "GINI: " * string(ginicoefficient(x)),
        label = "Lorenz curve" )
end

data = [20, 30, 40, 50, 60, 70, 80, 90, 120, 150]
ginicoefficient(data)
lorenz_curve(data)