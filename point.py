import math


class Point:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, other: float):
        return Point(self.x * other, self.y * other)

    def __truediv__(self, other: float):
        return Point(self.x / other, self.y / other)


def distance(p1: Point, p2: Point) -> float:
    return math.sqrt(
        math.pow(p1.x - p2.x, 2) + math.pow(p1.y - p2.y, 2)
        )


def get_point_by_k_b(k1: float, k2: float, b1: float, b2: float) -> Point:
    x = (b1 - b2) / (k2 - k1)
    y = k2 * x + b2
    return Point(x, y)
