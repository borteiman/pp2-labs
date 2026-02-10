is_prime = lambda n: n > 1 and all(n % i != 0 for i in range(2, int(n**0.5) + 1))

numbers = list(map(int, input().split()))
primes = list(filter(is_prime, numbers))

if primes:
    print(*(primes))
else:
    print("No primes")