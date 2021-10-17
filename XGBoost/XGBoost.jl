import Statistics: mean

function mse(y::Array, ytarget::Array, N::Integer = 0)
    if N == 0
        N = length(y)
    end
    return 1/N * sum((y .- ytarget) .^ 2)
end


mutable struct RegressionTree
    max_depth::Integer # максимальная глубина
    min_size::Integer # минимальный размер поддерева
    value::Number # значение в поддереве (среднее по всем листьям)
    feature_idx::Integer # номер лучшего признака
    feature_threshold::Number # значение лучшего признака
    left
    right
end

function maketree(max_depth=3, min_size=8,value=0,
                feature_idx=-1, feature_threshold=0,
                left=nothing, right=nothing)
    return RegressionTree(max_depth, min_size,value,
        feature_idx, feature_threshold, left, right)
end

function fit(tree::RegressionTree, X::Matrix, y::Array)
    tree.value = mean(y)
    N = size(y, 1)
    base_error = mse(y, ones(N) .* tree.value, N)
    error = base_error
    flag = 0
    error_left = base_error
    error_right = 0
        
    # если дошли до глубины 0 - выходим
    if tree.max_depth <= 1
        return
    end
    
    dim_shape = size(X, 2)
        
    # значения в левом и правом поддереве
    left_value = 0
    right_value = 0
        
    # начинаем цикл по признакам
    for feat = 1:dim_shape
        # сортируем признаки
        indexes = sortperm(X[:, feat])
        
        # количество сэмплов в левом и правом поддереве
        N = size(X, 1)
        N1, N2 = N-1, 1
        thres = 2
        # начинаем проходиться по значениям признака
        
        while thres < N
            N1 -= 1
            N2 += 1    
            idx = indexes[thres]
            x = X[idx, feat]
                
            # пропускаем одинаковые признаки
            if x == X[indexes[thres + 1], feat]
                thres += 1
                continue
            end
            
            # данные, которые получаются у нас в результате такого сплита
            target_right = y[indexes][1:thres]
            target_left = y[indexes][thres+1:end]
            mean_right = mean(target_right)
            mean_left = mean(target_left)
                
            # на этом шаге уже нужно считать ошибку - 
            # генерируем предикты (среднее в потомках)
            mean_right_array = ones(N2) * mean_right
            mean_left_array = ones(N1) * mean_left
                
            # считаем ошибку слева и справа
            error_right = mse(target_right, mean_right_array, N2)
            error_left = mse(target_left, mean_left_array, N1)
                
            # если выполняются условия сплита, то обновляем
            if (error_left + error_right) < error
                if min(N1, N2) > tree.min_size
                    tree.feature_idx = feat
                    tree.feature_threshold = x
                    left_value = mean_left
                    right_value = mean_right
                    flag = 1
                    error = error_left + error_right
                end
            end

            thres += 1
        end
        
        # если не нашли лучший сплит, выходим
        if tree.feature_idx == -1
            return
        end
        # дошли сюда - есть хорошее разбиение, нужно обучать дальше
        # инициализируем потомков - те же деревья решений
        tree.left = maketree(tree.max_depth - 1)
        tree.left.value = left_value
        tree.right = maketree(tree.max_depth - 1)
        tree.right.value = right_value
        
        # индексы потомков
        idxs_l = (X[:, tree.feature_idx] .> tree.feature_threshold)
        idxs_r = (X[:, tree.feature_idx] .<= tree.feature_threshold)
        
        # обучаем
        fit(tree.left, X[idxs_l, :], y[idxs_l])
        fit(tree.right, X[idxs_r, :], y[idxs_r])
    end
end
        
function _predict(tree::RegressionTree, x::AbstractArray)
    if tree.feature_idx == -1
        return tree.value
    end
    if x[tree.feature_idx] > tree.feature_threshold
        return _predict(tree.left, x)
    else
        return _predict(tree.right, x)
    end
end

        
function predict(tree, X::Matrix)
    return map(x -> _predict(tree, x), eachrow(X))
end
