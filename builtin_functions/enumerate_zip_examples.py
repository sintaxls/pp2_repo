# example 1 enumerate() and zip() for paired iteration

# fruits = ["banana", "apple", "orange"]
# prices = [100,200,300]

# print()
# print("enumerate()")
# for i, f in enumerate(fruits, start=1):
#     print(i, f)

# print()
# print("zip()")
# for f, p in zip(fruits, prices):
#     print(f,p)

# print()
# print("enumerate() and zip()")
# for i, (f,p) in enumerate(zip(fruits, prices), start=1):
#     print(f"{i}) {f} {p}")



# example 2 type checking and conversions

# type checking
# lst = ["10", 10, 10.0, True, ("a", "b"), [True, False]]

# for i in lst:
#     print(f"{i}: Type: {type(i)}")

# conversions
# str_int = "12"
# str_fl = "12.90"
# intnum = 12
# floatnum = 12.66

# print(int(str_int))
# print(float(str_fl))
# print(str(intnum))
# print(str(floatnum))
# print(bool(1))
# print(list("abcde"))