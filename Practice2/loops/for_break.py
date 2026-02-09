fruits = ["apple", "banana", "cherry"]
for x in fruits:
  print(x)
  if x == "banana":
    break
  
fruits = ["apple", "banana", "cherry"]
for x in fruits:
  if x == "banana":
    break
  print(x)

# The else block will NOT execute here
for x in range(6):
  if x == 3: break
  print(x)
else:
  print("Finally finished!")

