class ColoredPoint:
    def __init__(self, x, y, color):
        self._x = x
        self._y = y
        self._color = color

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def color(self):
        return self._color

    def __repr__(self):
        return f"ColoredPoint({self.x}, {self.y}, '{self.color}')"

    def __eq__(self, other):
        if not isinstance(other, ColoredPoint):
            return NotImplemented
        return (self.x, self.y, self.color) == (other.x, other.y, other.color)

    def __hash__(self):
        return hash((self.x, self.y, self.color))


# Пример использования
point1 = ColoredPoint(1, 2, "red")
point2 = ColoredPoint(1, 2, "red")
point3 = ColoredPoint(2, 3, "blue")

# Проверка строкового представления
print(repr(point1))  # ColoredPoint(1, 2, 'red')

# Проверка сравнения
print(point1 == point2)  # True
print(point1 == point3)  # False

# Проверка работы с hash
points_dict = {
    point1: "This is point1",
    point3: "This is point3"
}

print(points_dict[point2])  # This is point1
print(points_dict[point3])  # This is point3
