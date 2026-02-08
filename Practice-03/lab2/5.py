n = input()

numbers = list(map(int, input().split()))

mma = max(numbers)

print(numbers.index(mma) + 1)