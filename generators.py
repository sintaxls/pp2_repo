# 1. the squares of numbers up to some number N

def showsquares(n : int):
    for i in range(1, math.isqrt(n)+1):
        print(i**2, end=" ")

import math
n = int(input())
showsquares(n)



