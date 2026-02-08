def show(self):
    print(self.x, self.y)

def move(self, new_x, new_y):
    self.x = new_x
    self.y = new_y

def dist(self, pos_x, pos_y):
    print(sqrt((self.x - pos_x)**2 + (self.y - pos_y)**2))



def withdraw(self, amount):
    if self.total - amount < 0:
        print("No bro, you can't do that")
    else:
        self.total -= amount
        print(f"Balance after withdrawal: {self.total}")

def deposit(self, amount):
    self.total += amount
    print(f"Balance after deposit: {self.total}")


class Filter: 
    def __init__(self, num):
        self.num = num

    def is_prime(self, n):
        if n == 0 or n == 1:
            return False
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                return False
        return True

    def prime(self):
        return list(filter(lambda x: self.is_prime(x), self.num))

