a = int(input())
counts = {}

for i in range(a):
    bor = input().split()
    if bor[0] in counts:
        counts[bor[0]] += int(bor[1])
    
    else:
        counts[bor[0]] = int(bor[1])

for i in sorted(counts):
    print(counts[i], i)

#counts[i]