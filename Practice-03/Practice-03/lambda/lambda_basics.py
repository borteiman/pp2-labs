# Step 1: Add 10 to argument a, and return the result
x = lambda a : a + 10
print(x(5))

# Step 2: Multiply argument a with argument b
x = lambda a, b : a * b
print(x(5, 6))

# Step 3: Summarize arguments a, b, and c
x = lambda a, b, c : a + b + c
print(x(5, 6, 2))

# Step 4: Use lambda inside another function to create a doubler and tripler
def myfunc(n):
  return lambda a : a * n

mydoubler = myfunc(2)
mytripler = myfunc(3)

print(mydoubler(11))
print(mytripler(11))