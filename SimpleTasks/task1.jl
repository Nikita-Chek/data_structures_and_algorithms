w = 0

function findways(n::Int) ::Int
    if n == 1
        return 2
    elseif n == 2
        return 4
    elseif n == 0
        return 1
    end
    return findways(n-1) + findways(n-2) + findways(n-3)
end

print(findways(5))