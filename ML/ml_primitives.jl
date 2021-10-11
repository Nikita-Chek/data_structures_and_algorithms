function gini_impurity(p)
    return 1 - sum(p .^ 2)
end

function shannon_entropy(p)
    return  -sum(x .* log.(x))
end

