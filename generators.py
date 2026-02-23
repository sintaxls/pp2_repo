# 1. the squares of numbers up to some number N

# def showsquares(n : int):
#     for i in range(1, math.isqrt(n)+1):
#         print(i**2, end=" ")

# import math
# n = int(input())
# showsquares(n)



# 2. Write a program using generator to print the even numbers between 0 and n in comma separated form where n is input from console.

def evengenerator(n : int):
    for i in range(1,n+1,2):
        if i == n-1 or i == n:
            print(i, end="")
            break
    
        print(f"{i}, ",end="")

n = int(input())
evengenerator(n)