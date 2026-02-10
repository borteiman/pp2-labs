n = int(input())

if n <= 0:
    print("No")

else:
    for x in [2, 3, 5]:
        while n % x == 0:
            n //= x

    if n == 1:
        print("Yes")
    else:
        print("No")