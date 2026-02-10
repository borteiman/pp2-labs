n = int(input())
arr = list(map(int, input().split()))

a = int(input())

for i in range(a):
    command = input().split()
    op = command[0]

    if op == "add":
        val = int(command[1])
        arr = list(map(lambda x: x + val, arr))

    elif op == "multiply":
        val = int(command[1])
        arr = list(map(lambda x: x * val, arr))

    elif op == "power":
        val = int(command[1])
        arr = list(map(lambda x: x ** val, arr))

    elif op == "abs":
        arr = list(map(lambda x: abs(x), arr))

print(*arr)