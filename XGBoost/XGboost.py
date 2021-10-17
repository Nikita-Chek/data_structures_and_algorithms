import numpy as np
import sklearn.datasets
import sklearn

class RegressionTreeFastMse():
    
    '''
    Класс RegressionTree с быстрым пересчетом ошибки. Сложность пересчета ошибки
    на каждой итерации составляет O(1).
    '''
    
    # объявляем характеристики класса
    def __init__(self, max_depth=3, min_size=10):
        
        self.max_depth = max_depth
        self.min_size = min_size
        self.value = 0
        self.feature_idx = -1
        self.feature_threshold = 0
        self.left = None
        self.right = None
        
    # процедура обучения - сюда передается обучающая выборка
    def fit(self, X, y):
        
        # начальное значение - среднее значение y
        self.value = y.mean()
        # начальная ошибка - mse между значением в листе (пока нет
        # разбиения, это среднее по всем объектам) и объектами
        base_error = ((y - self.value) ** 2).sum()
        error = base_error
        flag = 0
        
        # пришли в максимальную глубину
        if self.max_depth <= 1:
            return
    
        dim_shape = X.shape[1]
        
        left_value, right_value = 0, 0
        
        for feat in range(dim_shape):
            
            prev_error1, prev_error2 = base_error, 0 
            idxs = np.argsort(X[:, feat])
            
            # переменные для быстрого переброса суммы
            mean1, mean2 = y.mean(), 0
            sm1, sm2 = y.sum(), 0
            
            N = X.shape[0]
            N1, N2 = N, 0
            thres = 1
            
            while thres < N - 1:
                N1 -= 1
                N2 += 1

                idx = idxs[thres]
                x = X[idx, feat]
                
                # вычисляем дельты - по ним в основном будет делаться переброс
                delta1 = (sm1 - y[idx]) * 1.0 / N1 - mean1
                delta2 = (sm2 + y[idx]) * 1.0 / N2 - mean2
                
                # увеличиваем суммы
                sm1 -= y[idx]
                sm2 += y[idx]
                
                # пересчитываем ошибки за O(1)
                prev_error1 += (delta1**2) * N1 
                prev_error1 -= (y[idx] - mean1)**2 
                prev_error1 -= 2 * delta1 * (sm1 - mean1 * N1)
                mean1 = sm1/N1
                
                prev_error2 += (delta2**2) * N2 
                prev_error2 += (y[idx] - mean2)**2 
                prev_error2 -= 2 * delta2 * (sm2 - mean2 * N2)
                mean2 = sm2/N2
                
                # пропускаем близкие друг к другу значения
                if thres < N - 1 and np.abs(x - X[idxs[thres + 1], feat]) < 1e-5:
                    thres += 1
                    continue
                
                # 2 условия, чтобы осуществить сплит - уменьшение ошибки 
                # и минимальное кол-о эл-в в каждом листе
                if (prev_error1 + prev_error2 < error):
                    if (min(N1,N2) > self.min_size):
                    
                        # переопределяем самый лучший признак и границу по нему
                        self.feature_idx, self.feature_threshold = feat, x
                        # переопределяем значения в листах
                        left_value, right_value = mean1, mean2

                        # флаг - значит сделали хороший сплит
                        flag = 1
                        error = prev_error1 + prev_error2
                                     
                thres += 1
 
        # ничего не разделили, выходим
        if self.feature_idx == -1:
            return
        
        self.left = RegressionTreeFastMse(self.max_depth - 1)
        # print ("Левое поддерево с глубиной %d"%(self.max_depth - 1))
        self.left.value = left_value
        self.right = RegressionTreeFastMse(self.max_depth - 1)
        # print ("Правое поддерево с глубиной %d"%(self.max_depth - 1))
        self.right.value = right_value
        
        idxs_l = (X[:, self.feature_idx] > self.feature_threshold)
        idxs_r = (X[:, self.feature_idx] <= self.feature_threshold)
    
        self.left.fit(X[idxs_l, :], y[idxs_l])
        self.right.fit(X[idxs_r, :], y[idxs_r])
        
    def __predict(self, x):
        if self.feature_idx == -1:
            return self.value
        
        if x[self.feature_idx] > self.feature_threshold:
            return self.left.__predict(x)
        else:
            return self.right.__predict(x)
        
    def predict(self, X):
        y = np.zeros(X.shape[0])
        
        for i in range(X.shape[0]):
            y[i] = self.__predict(X[i])
            
        return y



X,y = sklearn.datasets.fetch_covtype(data_home=None, download_if_missing=True, random_state=None, shuffle=True, return_X_y=True)

X, y = np.array(X), np.array(y)

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)


A = RegressionTreeFastMse(4, min_size=5)
A.fit(X_train,y_train)
test_mytree = A.predict(X_test) 

# np.savetxt('Xtrain.csv', X_train, delimiter=",")
# np.savetxt('Xtest.csv', X_test, delimiter=",")
# np.savetxt('ytrain.csv', y_train, delimiter=",")
# np.savetxt('ytest.csv', y_test, delimiter=",")
