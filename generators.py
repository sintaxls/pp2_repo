# 1. the squares of numbers up to some number N

# def showsquares(n : int):
#     for i in range(1, math.isqrt(n)+1):
#         print(i**2, end=" ")

# import math
# n = int(input())
# showsquares(n)



# 2. Write a program using generator to print the even numbers between 0 and n in comma separated form where n is input from console.

# def evengenerator(n : int):
#     for i in range(1,n+1,2):
#         if i == n-1 or i == n:
#             print(i, end="")
#             break
    
#         print(f"{i}, ",end="")

# n = int(input())
# evengenerator(n)


# 3. Define a function with a generator which can iterate the numbers, which are divisible by 3 and 4, between a given range 0 and n.

# def iteratediv34(n:int):
#     a = []
#     for i in range(3,n+1):
#         if i%3==0 and i%4==0:
#             yield i
#     # print(",".join(map(str, a)))

# n = int(input())
# for number in iteratediv34(n):
#     print(number)



# 4. Implement a generator called squares to yield the square of all numbers from (a) to (b). 
# Test it with a "for" loop and print each of the yielded values.

# def sq(a,b):
#     for i in range(a,b+1):
#         yield i*i
    
# for value in sq(1,5):
#     print(value)
