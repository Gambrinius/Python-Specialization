class Value:
    def __init__(self, value=0):
        self.value = value

    def __set__(self, instance, value):
        self.value = value * (1 - instance.commission)

    def __get__(self, instance, owner):
        return self.value


class Account:
    amount = Value()

    def __init__(self, commission):
        self.commission = commission


if __name__ == '__main__':
    acc = Account(0.1)
    acc.amount = 100
    print(acc.amount)
