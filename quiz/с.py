a = int(input())
count = {}
arr = list(map(int, input().split()))

for n in arr:
    if n in count:
        count[n] += 1
    
    else:
        count[n] = 1

max = 0
dig = arr[0]

for n in count:
    if count[n] > max:
        max = count[n]
        dig = n

    elif count[n] == max:
        if n < dig:
            dig = n

print(dig)