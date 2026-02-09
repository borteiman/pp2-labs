n = input()

numbers = map(int, input().split())

res = sum(1 for x in numbers if x > 0)

print(res)