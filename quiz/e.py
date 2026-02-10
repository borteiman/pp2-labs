# Функция для проверки, простое ли число
def is_prime(n):
    if n < 2: return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

nums = list(map(int, input().split()))

# Используем filter и lambda
primes = list(filter(lambda x: is_prime(x), nums))

if not primes:
    print("No primes")
else:
    print(*primes)