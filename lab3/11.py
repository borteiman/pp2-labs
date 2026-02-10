class Pair:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def add(self, other):
        a_sum = self.a + other.a
        b_sum = self.b + other.b
        return f"Result: {a_sum} {b_sum}"

data = list(map(int, input().split()))
p1 = Pair(data[0], data[1])
p2 = Pair(data[2], data[3])

print(p1.add(p2))