n = int(input())

nums = list(map(int, input().split()))

res = sorted(nums)
print(*reversed(res))