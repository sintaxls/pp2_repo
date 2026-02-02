# Do not print banana:

fruits = ["apple", "banana", "cherry"]
for x in fruits:
  if x == "banana":
    continue
  print(x)

# skip even numbers
# numbers = [1, 2, 3, 4, 5, 6]
# for n in numbers:
#   if n % 2 == 0:
#     continue
#   print(n)

# skip empty strings
# words = ["hello", "", "world", ""]
# for w in words:
#   if w == "":
#     continue
#   print(w)

# skip short names
# names = ["Al", "Bob", "Cara", "Di"]
# for name in names:
#   if len(name) < 3:
#     continue
#   print(name)

# skip items containing a digit
# items = ["box", "item2", "pack", "3rd"]
# for item in items:
#   if any(ch.isdigit() for ch in item):
#     continue
#   print(item)