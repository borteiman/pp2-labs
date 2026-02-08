a, b, c = map(int, input().split())

nums = list(map(int, input().split()))

nums[b - 1:c] = nums[b - 1:c][::-1]

print(*nums)