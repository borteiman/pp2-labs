n = int(input())

numbers = list(map(int, input().split()))

mmax = max(numbers)
mmin = min(numbers)

for i in range(n):
    if numbers[i] == mmax:
        numbers[i] = mmin

print(*numbers)    