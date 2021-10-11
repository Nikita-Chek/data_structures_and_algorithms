def fib(a):
    m = 0
    n = 1
    while m < a:
        s = m + n
        n = m
        m = s
    return n

print(fib(6))