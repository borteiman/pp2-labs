n = int(input())

nums = list(map(int, input().split()))

for i in range(n):
    nums[i] *= nums[i]

print(*nums)