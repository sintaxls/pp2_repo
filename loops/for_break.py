# Exit the loop when x is "banana":
fruits = ["apple", "banana", "cherry"]
for x in fruits:
  print(x)
  if x == "banana":
    break
  
# Exit the loop when x is "banana", but this time the break comes before the print:

# fruits = ["apple", "banana", "cherry"]
# for x in fruits:
#   if x == "banana":
#     break
#   print(x)

# Stop when a number is greater than 3
# numbers = [1, 2, 3, 4, 5]
# for n in numbers:
#   if n > 3:
#     break
#   print(n)

# Stop when a word starts with "b"
# words = ["apple", "berry", "cherry", "date"]
# for w in words:
#   if w.startswith("b"):
#     break
#   print(w)

# Stop when encountering a specific letter
# letters = ["a", "c", "e", "x", "z"]
# for letter in letters:
#   if letter == "x":
#     break
#   print(letter)