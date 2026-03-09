# example 1
with open("file_handling/examplefile.txt", "a") as f:
  f.write("Now the file has more content!")

with open("file_handling/examplefile.txt") as f:
  print(f.read())