class A:
    def __init__(self, b: dict = {}) -> None:
        self.b = b


a1 = A()
a2 = A()

print(a1.b)
print(a2.b)

a1.b["test"] = 123

print(a1.b)
print(a2.b)
