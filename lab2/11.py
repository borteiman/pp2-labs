n = int(input())

if n == 2:
    print("Yes")

elif n < 2 or n % 2 == 0:
    print("No")

else:
    for i in range(3, int(n ** 0.5) + 1, 2):
        if n % i == 0:
            print("No")
            break

    else:
        print("Yes")