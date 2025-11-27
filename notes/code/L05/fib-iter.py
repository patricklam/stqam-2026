def fib(n):
    a = 1
    b = 1
    next = b  
    count = 1
    seq = [1, 1]

    while count <= n:
        count += 1
        a, b = b, next
        next = a + b
        seq.append(next)
    return seq

print (fib(10))
