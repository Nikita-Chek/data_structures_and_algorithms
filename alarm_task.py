"""
Original task : https://yandex.ru/cup/backend/analysis/

A. Будильники
"""

n_alarms = lambda T, t, X: sum( map( lambda ti: max((T - ti) // X + 1, 0), t) )


def drop_extra_alarms(t: list, X: int):

    mods = {i: i % X for i in t}
    
    mods_sorted = sorted(mods.items(), key=lambda x: (x[1], x[0]))
    
    i = 1
    while i < len(mods_sorted):
    
        if mods_sorted[i-1][1] == mods_sorted[i][1]:
            del mods_sorted[i]
            i -= 1
    
        i += 1
    
    return [i[0] for i in mods_sorted]

def binary_search(t, X, K):
    T_max = min(t) + K * X
    T_min = 0
    T_mid = 0
    res = 0
    while T_min <= T_max:
     
        T_mid = (T_max + T_min) // 2

        k_to_find = n_alarms(T_mid, t, X)
        
        if k_to_find < K:
            T_min = T_mid + 1
            
        elif k_to_find > K:
            T_max = T_mid - 1 
            
        else:
            res =  T_mid
            T_max = T_mid - 1
    return res

N, X, K = (int(_) for _ in input().split())
t = [int(_) for _ in input().split()]
t = drop_extra_alarms(t, X)
print(binary_search(t, X, K))

# from numpy import random
# t = random.randint(10**9, size=(10**6))
# X = random.randint(10**3)
# K = random.randint(10**9)
# t = drop_extra_alarms(t, X)
# print("answer: ", binary_search(t, X, k))