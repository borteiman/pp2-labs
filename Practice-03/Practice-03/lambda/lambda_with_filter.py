# Step 1: Define a list of numbers
numbers = [1, 2, 3, 4, 5, 6, 7, 8]

# Step 2: Filter out even numbers (keep odd numbers) using filter() and lambda
odd_numbers = list(filter(lambda x: x % 2 != 0, numbers))

# Step 3: Output the result
print(odd_numbers)





# Example 1: Filter out even numbers (keep odd numbers)
# Step 1: Define a list of numbers
numbers = [1, 2, 3, 4, 5, 6, 7, 8]
# Step 2: Use filter() to keep numbers where remainder is not 0
odd_numbers = list(filter(lambda x: x % 2 != 0, numbers))
print(odd_numbers)

# Example 2: Filter words longer than 5 characters
# Step 1: Define a list of words
words = ["cat", "elephant", "dog", "giraffe"]
# Step 2: Use filter() to keep only words with length greater than 5
long_words = list(filter(lambda w: len(w) > 5, words))
# Step 3: Print the filtered words
print(long_words)

# Example 3: Filter positive numbers
# Step 1: Define a list with mixed positive and negative numbers
mixed_numbers = [-10, 5, -3, 8, 0, 12]
# Step 2: Use filter() to keep only numbers strictly greater than 0
positive_numbers = list(filter(lambda n: n > 0, mixed_numbers))
# Step 3: Print the positive numbers
print(positive_numbers)