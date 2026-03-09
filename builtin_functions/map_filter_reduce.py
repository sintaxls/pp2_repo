# example 1 map() and filter() on lists
# nums = [1,2,3,4,5,6,7]

# sqared = list(map(lambda x: x*x, nums))
# even = list(filter(lambda x: x%2 == 0, nums))

# print("sqared:", sqared)
# print("even:", even)



# example 2 Aggregate with reduce() (from functools)

# from functools import reduce
# nums = [1,2,3,4,5,6,7]

# total = reduce(lambda a, b: a+b, nums)
# product = reduce(lambda a,b: a*b, nums)

# print("sum:", total)
# print("product:", product)

