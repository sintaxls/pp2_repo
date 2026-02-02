# Continue to the next iteration if i is 3:

i = 0
while i < 6:
  i += 1
  if i == 3:
    continue
  print(i)

# Skip even numbers:
# n = 0
# while n < 10:
#   n += 1
#   if n % 2 == 0:
#     continue
#   print(n)


# Skip multiples of 3
# m = 0
# while m < 12:
#   m += 1
#   if m % 3 == 0:
#     continue
#   print(m)


# Skip a specific character
# word = "python"
# idx = 0
# while idx < len(word):
#   ch = word[idx]
#   idx += 1
#   if ch == "h":
#     continue
#   print(ch)


# Skip negative values
# values = [3, -1, 2, -5, 4]
# pos = 0
# while pos < len(values):
#   v = values[pos]
#   pos += 1
#   if v < 0:
#     continue
#   print(v)