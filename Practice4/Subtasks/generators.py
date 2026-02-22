#1
def square(n):
    for i in range(n+1):
        yield i*i

n = int(input())

squared = square(n)
for n in squared:
    print(n)

#2
def even(n):
    for i in range(n+1):
        if i % 2 == 0:
            yield i

n = int(input())

result = ", ".join(str(x) for x in even(n))
print(result)

#3
def divisible_by_3_and_4(n):
    # Генератор чисел, кратных и 3 и 4 (то есть 12)
    for i in range(n + 1):
        if i % 12 == 0:
            yield i


# example
n = 50
for num in divisible_by_3_and_4(n):
    print(num)

#4
def squares(a, b):
    for i in range(a, b + 1):
        yield i * i


# тест через for
a = 2
b = 6

for value in squares(a, b):
    print(value)

#5

def countdown(n):
    # Генератор, который идет от n вниз до 0
    while n >= 0:
        yield n
        n -= 1  # уменьшаем число


#example
n = 5
for num in countdown(n):
    print(num)
