# using CSV, DataFrames

# Xtrain = CSV.File("c:/Users/admin/Documents/XXX/data_structures_and_algorithms/XGBoost/Xtrain.csv", header=false) |> DataFrame |> Matrix
# Xtest = CSV.File("c:/Users/admin/Documents/XXX/data_structures_and_algorithms/XGBoost/Xtest.csv", header=false) |> DataFrame |> Array
# ytrain = CSV.File("c:/Users/admin/Documents/XXX/data_structures_and_algorithms/XGBoost/ytrain.csv", header=false) |> DataFrame |> Matrix
# ytest = CSV.File("c:/Users/admin/Documents/XXX/data_structures_and_algorithms/XGBoost/ytest.csv", header=false) |> DataFrame |> Array

# tree = maketree()
# fit(tree, Xtrain, ytrain)
pred = predict(tree, Xtest) 