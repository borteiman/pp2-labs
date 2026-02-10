n = int(input())
arr = list(map(int, input().split()))
q = int(input())

ops = {
    "add": lambda a, x: a + x,
    "multiply": lambda a, x: a * x,
    "power": lambda a, x: a ** x,
    "abs": lambda a, _: abs(a)
}

for _ in range(q):
    query = input().split()
    op_name = query[0]
    x = int(query[1]) if len(query) > 1 else None
    
    arr = [ops[op_name](item, x) for item in arr]

print(*(arr))