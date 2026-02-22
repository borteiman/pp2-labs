import math

degree = 15

# переводим градусы в радианы
radian = degree * math.pi / 180

# форматируем до 6 знаков после запятой
print("Output radian:", format(radian, ".6f"))

#2

height = 5
base1 = 5
base2 = 6

area = (base1 + base2) / 2 * height

print("Expected Output:", area)

#3

import math

n = 4
s = 25

# формула площади правильного многоугольника
area = (n * s ** 2) / (4 * math.tan(math.pi / n))

print("The area of the polygon is:", int(area))

#4

base = 5
height = 6

area = base * height

print("Expected Output:", float(area))


