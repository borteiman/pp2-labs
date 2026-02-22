class Account:
    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        # Пополнение счета
        self.balance += amount

    def withdraw(self, amount):
        # Снятие денег
        if amount > self.balance:
            # Если хотим снять больше, чем есть — возвращаем "Ничего"
            return None
        # Если денег хватает — вычитаем и возвращаем остаток
        self.balance -= amount
        return self.balance