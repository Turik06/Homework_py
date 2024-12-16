from functools import singledispatchmethod

class Negator:
    def __init__(self):
        pass

    @singledispatchmethod
    def neg(self, arg):
        raise TypeError(f"Аргумент типа {type(arg).__name__} не поддерживается")

    @neg.register(int)
    def _(self, arg):
        return arg * -1

    @neg.register(float)
    def _(self, arg):
        return arg * -1

    @neg.register(bool)
    def _(self, arg):
        return not arg

# Пример использования
ng = Negator()

print(ng.neg(10))       # Вывод: -10
print(ng.neg(-3.14))    # Вывод: 3.14
print(ng.neg(True))     # Вывод: False
print(ng.neg(False))    # Вывод: True

# Обработка неподдерживаемого типа
try:
    print(ng.neg([0, 1, 2, 3, 4, 5]))
except TypeError as e:
    print(e)  # Вывод: Аргумент типа list не поддерживается
